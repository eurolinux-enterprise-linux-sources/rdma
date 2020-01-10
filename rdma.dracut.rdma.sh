#!/bin/bash
CONFIG=/etc/rdma/rdma.conf

LOAD_ULP_MODULES=""
LOAD_CORE_USER_MODULES="ib_umad ib_uverbs ib_ucm rdma_ucm"
LOAD_CORE_CM_MODULES="iw_cm ib_cm rdma_cm"
LOAD_CORE_MODULES="ib_addr ib_core ib_mad ib_sa"

if [ -f $CONFIG ]; then
    . $CONFIG

    if [ "${RDS_LOAD}" = "yes" ]; then
        IPOIB_LOAD=yes
    fi

    if [ "${IPOIB_LOAD}" = "yes" ]; then
	LOAD_ULP_MODULES="ib_ipoib"
    fi

    if [ "${RDS_LOAD}" = "yes" ]; then
	LOAD_ULP_MODULES="$LOAD_ULP_MODULES rds"
    fi

    if [ "${SRP_LOAD}" = "yes" ]; then
	LOAD_ULP_MODULES="$LOAD_ULP_MODULES ib_srp"
    fi

    if [ "${ISER_LOAD}" = "yes" ]; then
	LOAD_ULP_MODULES="$LOAD_ULP_MODULES ib_iser"
    fi
else
    LOAD_ULP_MODULES="ib_ipoib"
fi

# If module $1 is loaded return - 0 else - 1
is_module()
{
    /sbin/lsmod | grep -w "$1" > /dev/null 2>&1
    return $?    
}

load_modules()
{
    for module in $*; do
    	is_module $module
    	RC=$?
	if [ ! $RC ]; then
	    /sbin/modprobe $module
	fi
    done
}

check_mtrr_registers()
{
    if [ -f /proc/mtrr -a -f /etc/rdma/fixup-mtrr.awk ]; then
	awk -f /etc/rdma/fixup-mtrr.awk /proc/mtrr 2>/dev/null
    	is_module ib_ipath
    	RC=$?
	if [ $RC ]; then
		/sbin/rmmod ib_ipath
		/sbin/modprobe ib_ipath
	fi
    	is_module ib_qib
    	RC=$?
	if [ $RC ]; then
		/sbin/rmmod ib_qib
		/sbin/modprobe ib_qib
	fi
    fi
}

load_hardware_modules()
{
    if [ "$FIXUP_MTRR_REGS" = "yes" ]; then
    	check_mtrr_registers
    fi
    if [ -r /proc/device-tree ]; then
	if [ -n "`ls /proc/device-tree | grep lhca`" ]; then
	    is_module ib_ehca
	    RC=$?
	    if [ ! $RC ]; then
		load_modules ib_ehca
	    fi
	fi
    fi
    is_module cxgb3
    RC1=$?
    is_module iw_cxgb3
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
	load_modules iw_cxgb3
    fi
    is_module cxgb4
    RC1=$?
    is_module iw_cxgb4
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
	load_modules iw_cxgb4
    fi
    is_module mlx4_core
    RC1=$?
    is_module mlx4_ib
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
	load_modules mlx4_ib
    fi
    is_module mlx5_core
    RC1=$?
    is_module mlx5_ib
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
	load_modules mlx5_ib
    fi
    is_module be2net
    RC1=$?
    is_module ocrdma
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
    	load_modules ocrdma
    fi
    is_module enic
    RC1=$?
    is_module usnic_verbs
    RC2=$?
    if [ $RC1 -ne $RC2 ]; then
    	load_modules usnic_verbs
    fi
}

start()
{
    load_hardware_modules
    load_modules $LOAD_CORE_MODULES
    load_modules $LOAD_CORE_CM_MODULES
    load_modules $LOAD_CORE_USER_MODULES
    load_modules $LOAD_ULP_MODULES
}

start
