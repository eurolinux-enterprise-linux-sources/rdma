#  Copyright (c) 2008 Red Hat, Inc.

#  There is no URL or upstream source entry as this package constitutes
#  upstream for itself.
%global rdma_moddir %{_datadir}/dracut/modules.d/10rdma

Summary: Infiniband/iWARP Kernel Module Initializer
Name: rdma
Version: 6.9_4.1
Release: 3%{?dist}
License: GPLv2+
Group: System Environment/Base
Source0: rdma.conf
Source1: rdma.init
Source2: rdma.fixup-mtrr.awk
Source3: rdma.rules
Source4: rdma.ifup-ib
Source5: rdma.nfs-rdma.init
Source6: rdma.ifdown-ib
Source7: rdma.dracut.check
Source8: rdma.dracut.install
Source9: rdma.dracut.installkernel
Source10: rdma.dracut.rdma.sh
Source11: rdma.mlx4-sysmodprobe
Source12: rdma.mlx4-usermodprobe
Source13: rdma.mlx4.conf
Source14: rdma.mlx4-setup.sh
Source15: rdma.cxgb3-sysmodprobe
Source16: rdma.cxgb4-sysmodprobe
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires(post): chkconfig
Requires(preun): chkconfig
Requires: udev >= 145
Requires: dracut, pciutils
Conflicts: libmlx4 < 1.0.6-7.el6, libcxgb3 < 1.3.1-3.el6, libcxgb4 < 1.3.5-1.el6
%description 
User space initialization scripts for the kernel InfiniBand/iWARP drivers

%prep

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/modprobe.d
install -d %{buildroot}/lib/udev/rules.d
install -d %{buildroot}%{_sysconfdir}/sysconfig/network-scripts
install -d %{buildroot}%{rdma_moddir}
install -d %{buildroot}%{_libexecdir}

install -m 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/fixup-mtrr.awk
install -m 0644 %{SOURCE3} %{buildroot}/lib/udev/rules.d/90-infiniband.rules
install -m 0755 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
install -m 0755 %{SOURCE5} %{buildroot}%{_initrddir}/nfs-rdma
install -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
install -m 0755 %{SOURCE7} %{buildroot}%{rdma_moddir}/check
install -m 0755 %{SOURCE8} %{buildroot}%{rdma_moddir}/install
install -m 0755 %{SOURCE9} %{buildroot}%{rdma_moddir}/installkernel
install -m 0755 %{SOURCE10} %{buildroot}%{rdma_moddir}/rdma.sh
install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/modprobe.d/libmlx4.conf
install -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/modprobe.d/mlx4.conf
install -m 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/%{name}/mlx4.conf
install -m 0755 %{SOURCE14} %{buildroot}%{_libexecdir}/mlx4-setup.sh
install -m 0644 %{SOURCE15} %{buildroot}%{_sysconfdir}/modprobe.d/libcxgb3.conf
install -m 0644 %{SOURCE16} %{buildroot}%{_sysconfdir}/modprobe.d/libcxgb4.conf

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
    /sbin/chkconfig --add %{name}
    /sbin/chkconfig --add nfs-rdma
else
    /sbin/chkconfig --list nfs-rdma >/dev/null 2>&1
    MISSING=$?
    if [ "$MISSING" = 0 ]; then
	chkconfig --level 0123456 nfs-rdma resetpriorities
    else
	chkconfig --add nfs-rdma
    fi
fi

%preun
if [ $1 = 0 ]; then
    # In case this script was never added, be silent
    /sbin/chkconfig --del nfs-rdma >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/mlx4.conf
%{_sysconfdir}/%{name}/fixup-mtrr.awk
%{_initrddir}/%{name}
%{_initrddir}/nfs-rdma
%{_sysconfdir}/sysconfig/network-scripts/ifup-ib
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ib
%{_sysconfdir}/modprobe.d/libmlx4.conf
%{_sysconfdir}/modprobe.d/libcxgb?.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%{_libexecdir}/mlx4-setup.sh
/lib/udev/rules.d/90-infiniband.rules
%{rdma_moddir}

%changelog
* Tue Nov 22 2016 Jarod Wilson <jarod@redhat.com> - 6.9_4.1-3
- Add support for including Mellanox drivers under kernel-rt
- Resolves: rhbz#1389554

* Tue Nov 01 2016 Jarod Wilson <jarod@redhat.com> - 6.9_4.1-2
- Don't try to load modules that don't exist
- Resolves: rhbz#1388061

* Wed Aug 10 2016 Jarod Wilson <jarod@redhat.com> - 6.9_4.1-1
- Default initscript to enabled for IPoIB setups
- Resolves: rhbz#1116631

* Fri Mar 18 2016 Donald Dutile <ddutile@redhat.com> - 6.8_4.1-1
- Add CMDLINE_OPTS for cxgb modules
- Resolves: bz1205092

* Wed May 20 2015 Doug Ledford <dledford@redhat.com> - 6.7_3.15-5
- Add requires on pciutils
- Resolves: bz1236042

* Tue May 19 2015 Doug Ledford <dledford@redhat.com> - 6.7_3.15-4
- Fix modprobe file so command line opts passed to modprobe mlx4_core will
  work again
- Resolves: bz1215857

* Thu Mar 12 2015 Doug Ledford <dledford@redhat.com> - 6.7_3.15-3
- A few touchups to the move of dracut files and such
- Related: bz1163527

* Thu Mar 12 2015 Doug Ledford <dledford@redhat.com> - 6.7_3.15-2
- Fix ipoib MTU issue
- Fix shutdown ordering of NFSoRDMA code
- Absorb mlx4/cxgb3/cxgb4 setup/module init code into our package
- Resolves: bz1186498, bz1163527

* Fri Jan 23 2015 Doug Ledford <dledford@redhat.com> - 6.7_3.15-1
- Fix module unload issue
- Resolves: bz1159331

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 6.6_3.15-1
- Change numbering scheme to be clearer: first number is redhat
  release this package is for (aka rhel6.6), second number is the
  upstream kernel that our kernel code comes from, aka 3.15.
- Minor fix to init script to support cxgb4 and ocrdma and mlx5
  drivers properly
- Add a dracut module to make sure all the needed InfiniBand
  kernel modules and support files make it on to the initrd
- Resolves: 1064308

* Wed Aug 07 2013 Doug Ledford <dledford@redhat.com> - 3.10-3
- Replace an errant usage of PARENTDEVICE with PHYSDEV in ifdown-ib
- Related: bz990288

* Wed Aug 07 2013 Doug Ledford <dledford@redhat.com> - 3.10-2
- Somehow during editing I accidentally deleted a single character from
  the post scriptlet.  rpmdiff caught it, now I'm fixing it.
- Resolves: bz990288

* Tue Jul 23 2013 Doug Ledford <dledford@redhat.com> - 3.10-1
- Bump version to match final kernel submission
- Add support for P_Key interfaces to ifup-ib and ifdown-ib

* Sun Oct 14 2012 Doug Ledford <dledford@redhat.com> - 3.6-1
- Bump version to match final kernel submission

* Fri Sep 14 2012 Doug Ledford <dledford@redhat.com> - 3.6-0.rc5.1
- Bump version to match kernel update submitted for rhel6.4

* Fri Aug 24 2012 Doug Ledford <dledford@redhat.com> - 3.3-4
- Fix an issue in the ifup-ib script
- Fix a problem with the setting of infiniband dev perms
- Resolves: bz834428

* Thu Apr 26 2012 Doug Ledford <dledford@redhat.com> - 3.3-3
- The fix to bug 808600 was noisy and resulted in bug 815999,
  silence the script
- Resolves: bz815999

* Tue Apr 24 2012 Doug Ledford <dledford@redhat.com> - 3.3-2
- Unload the iw_cxgb4 module when stopping the rdma stack
- Related: bz815622

* Tue Apr 24 2012 Doug Ledford <dledford@redhat.com> - 3.3-1
- Fix an issue in the rdma script that caused rds_rdma to load
  when it shouldn't
- Resolves: bz815622

* Thu Apr 05 2012 Doug Ledford <dledford@redhat.com> - 1.0-21
- Don't change the user's directory on interactive runs
- Related: bz808600

* Thu Apr 05 2012 Doug Ledford <dledford@redhat.com> - 1.0-20
- Name the cards slightly differently (upstream request)
- Check for the ibacm program before trying to down the stack
- Resolves: bz808600

* Thu Mar 22 2012 Doug Ledford <dledford@redhat.com> - 1.0-19
- Remove the rules file again, issue turned out to be a kernel bug.
- Related: bz739138

* Wed Mar 21 2012 Doug Ledford <dledford@redhat.com> - 1.0-18
- Resurrect rules file, some of the IB devices are not created by the
  kernel
- Related: bz739138

* Fri Mar 09 2012 Doug Ledford <dledford@redhat.com> - 1.0-17
- Don't do lsmod in the %%post script looking for ib_ipoib, anaconda
  loads it unconditionally.  Instead, anaconda has been modified to
  enable our init script if it installed over an IPoIB interface, so
  simply remove that portion of our %%post script.
- Related: bz739138

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0-16
- If we are being installed on a machine that has ib_ipoib module loaded,
  then this is likely because it is a machine being installed over IPoIB,
  so enable our init script
- Related: bz739138

* Tue Feb 28 2012 Doug Ledford <dledford@redhat.com> - 1.0-15
- No longer provide a rules file to create infinband devices, the kernel
  now creates them in the proper place all by itself
- Change the LSB headers in the init script, they were wrong
- Related: bz739138

* Tue Oct 25 2011 Doug Ledford <dledford@redhat.com> - 1.0-14
- Clear the umask before loading kernel modules otherwise the kernel
  modules inherit our umask and don't create the /dev/infiniband
  files with the proper permissions.
- Resolves: bz748087

* Wed Oct 19 2011 Doug Ledford <dledford@redhat.com> - 1.0-13
- Default to not loading the RDS stack by default as it has some known
  issues at the moment.
- Resolves: bz747378

* Thu Aug 11 2011 Doug Ledford <dledford@redhat.com> - 1.0-12
- Another minor fix to RDS support in the rdma script
- Related: bz725016

* Thu Aug 04 2011 Doug Ledford <dledford@redhat.com> - 1.0-11
- Minor fix to RDS support in the rdma init script
- Related: bz725016

* Thu Aug 04 2011 Doug Ledford <dledford@redhat.com> - 1.0-10
- Fix ifup-ib script to be compatible with change to core function
  expand_config
- Fix renaming of ib? devices to the name given in the ifcfg-* file
- Fix the fact that once you down the rdma stack and reload it, the
  HWADDR line in ifcfg-* files no longer matches the address of the
  ports.  We now match only on the part of the HWADDR that doesn't
  change.
- Fix rdma init script to know about cxgb4 adapters
- Fix rdma init script to find all InfiniBand interfaces whether they
  use an ib? name or a custom name
- Fix rdma init script to down all InfiniBand interfaces on rdma shutdown
  regardless of interface name
- Fix rdma init script to find all ifcfg-* files that apply to ipoib
  interfaces without requiring that they be named ib?
- Fix rdma init script to know to unload ib_qib module on stop
- Add an ifdown-ib file that fixes the HWADDR not matching on the second
  or later times you down the rdma subsystem
- Related: bz725016
- Resolves: bz678947, bz721101

* Tue Aug 17 2010 Doug Ledford <dledford@redhat.com> - 1.0-9
- Minor tweak to rdma init script to do the udevadm trigger command in two
  seperate calls since we can no longer match on the same item twice and
  have the command succeed for both match types.
- Resolves: bz612234

* Wed Aug 04 2010 Doug Ledford <dledford@redhat.com> - 1.0-8
- Update udev rules syntax to eliminate warnings emitted via syslog (bz603264)
- Add new init script for starting/stopping nfs over rdma support
- Require that the nfs-rdma service be down before stopping the rdma
  service (bz613437)
- Change ifup-ib to properly account for the fact that the [ test program
  does not process tests in order and fail immediately on first failing
  test, resulting in error messages due to unquoted environment variables
  that don't need quoting in the second test due to the fact that the
  first test guarantees they exist.  Or that's how things should be, but
  they aren't, so rewrite tests to accommodate this fact. (bz612284)
- Use ip instead of ifconfig as ifconfig knows it doesn't handle infinband
  hardware addresses properly (even though we don't care, we aren't using
  it for that) and prints out copious warning messages (bz613086)
- Related: bz612284, bz613086

* Wed May 26 2010 Doug Ledford <dledford@redhat.com> - 1.0-7
- Require a version of udev that's known to contain udevadm and support
  usage of udevadm trigger and udevadm settle
- Update rdma.init to use the proper udev commands
- Resolves: bz586594

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0-6
- Tweak init script for LSB compliance
- Tweak ifup-ib script to work properly with bonded slaves that need their
  MTU set
- Tweak ifup-ib script to properly change connected mode either on or off
  instead of only setting it on but not turning it off if the setting changes

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-3
- Add the ifup-ib script so we support connected mode on ib interfaces

* Mon Jun 09 2008 Doug Ledford <dledford@redhat.com> - 1.0-2
- Attempt to use --subsystem-match=infiniband in the rdma init script use
  of udevtrigger so we don't trigger the whole system
- Add a requirement to stop opensm to the init script

* Sun Jun 08 2008 Doug Ledford <dledford@redhat.com> - 1.0-1
- Create an initial package for Fedora review

