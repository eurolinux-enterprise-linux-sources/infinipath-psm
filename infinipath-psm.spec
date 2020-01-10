# infinipath-psm
%global git_version 22_g4abbc60_open
%global _hardened_build 1
%global MAKEARG PSM_HAVE_SCIF=0 MIC=0

Summary: QLogic PSM Libraries
Name: infinipath-psm
Version: 3.3
Release: %{git_version}.2%{?dist}
License: BSD or GPLv2
ExclusiveArch: x86_64
Group: System Environment/Libraries
# For information on OpenFabrics Alliance, which this package is a member of
URL: https://www.openfabrics.org/
# The upstream git repo
# git://github.com/01org/psm
# The exact hash we used to create our local tarball
# 4abbc60ab02c51efee91575605b3430059f71ab8
Source0: %{name}-%{version}-%{git_version}.tar.gz
Source1: ipath.rules
Patch1: misleading-indentation.patch
Patch2: remove-executable-permissions-for-header-files.patch
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=56977
Patch3: disable-Werror.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: udev
BuildRequires: gcc
BuildRequires: libuuid-devel
Conflicts: infinipath-libs <= %{version}-%{release}
Obsoletes: libpsm2-compat

%package devel
Summary: Development files for QLogic PSM
Group: System Environment/Development
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: libuuid-devel
Conflicts: infinipath-devel <= %{version}-%{release}

%description
The PSM Messaging API, or PSM API, is QLogic's low-level
user-level communications interface for the Truescale
family of products. PSM users are enabled with mechanisms
necessary to implement higher level communications
interfaces in parallel environments.

%description devel
Development files for the libpsm_infinipath library

%prep
%setup -q -n infinipath-psm-%{version}-%{git_version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
find libuuid -type f -not -name 'psm_uuid.[c|h]' -not -name Makefile -delete

%build
export CFLAGS="$RPM_OPT_FLAGS"
%make_build PSM_USE_SYS_UUID=1 %{MAKEARG} CC=gcc

%install
%make_install %{MAKEARG}
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/udev/rules.d/60-ipath.rules

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%{_sysconfdir}/udev/rules.d/60-ipath.rules
%{_libdir}/libpsm_infinipath.so.*
%{_libdir}/libinfinipath.so.*
%license COPYING
%doc README

%files devel
%{_libdir}/libpsm_infinipath.so
%{_libdir}/libinfinipath.so
%{_includedir}/psm.h
%{_includedir}/psm_mq.h

%changelog
* Tue May 31 2016 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.2
- Obsoletes libpsm2-compat.
- Related: bz1272022

* Thu Apr 21 2016 Honggang Li <honli@redhat.com> - 3.3-22_g4abbc60_open.1
- Rebase to latest upstream release.
- Link against system libuuid library.
- Spec file cleanup.
- Related: bz1272022

* Mon Oct 27 2014 Doug Ledford <dledford@redhat.com> - 3.3-0.g6f42cdb1bb8.2
- Fix missing FORTIFY_SOURCE setting
- Related: bz1085255

* Mon Oct 27 2014 Doug Ledford <dledford@redhat.com> - 3.3-0.g6f42cdb1bb8.1
- Update from upstream git repo
- Resolves: bz1085255

* Mon Mar 3 2014 Jay Fenlason <fenlason@redhat.com> -3.2-2_ga8c3e3e_open.2
- Update the -build patch and this spec file so the library is built
  with the standard optimization and security flags.
  Resolves: rhbz1070814

* Thu Jan 16 2014 Jay Fenlason <fenlason@redhat.com> -3.2-2_ga8c3e3e_open.1
- New upstream version
  Resolves: rhbz727555

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.1-4.r364.1140_open
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Jay Fenlason <fenlason@redhat.com> 3.1-3.r364.1140_open
- Fix the path to the udev file to close
  Resolves: rhbz1034508 - [RHEL-7.0] /dev/ipath* permissions are wrong

* Thu Feb 7 2013 jay Fenlason <fenlason@redhat.com> 3.1-2.r364.1140_open
- Pull in upstream patch to close
  Resolves: rhbz907730 - [RHEL-7.0] libpsm_infinipath.so: undefined reference to knem_open_device

* Mon Dec 10 2012 Jay Fenlason <fenlason@redhat.com> 3.1-1
- Upgrade to new upstream version.
- add the -edata patch to handle the type-change of the edata sypmbol
  from 'A' to 'D'.

* Tue May 29 2012 Jay Fenlason <fenlason@redhat.com> - 2.9-926.1005_open.3
- Add the -warnings patch to allow building on RHEL-7.
  Resolves: rhbz818841

* Mon Feb 6 2012 Jay Fenlason <fenlason@redhat.com> -  2.9-926.1005_open.2
- Add the udev rules file to close
  Resolves: rhbz747406

* Mon Jul 25 2011 Jay Fenlason <fenlason@redhat.com> - 2.9-926.1005_open.1
- New upstream version.
  Resolves: rhbz635915

* Fri Nov 5 2010 Jay Fenlason <fenlason@redhat.com>
- Include the -execstack patch to get libinfinipath.so correctly
  labeled as not executing the stack.
  Resolves: rhbz612936

* Thu Jun 3 2010 Jay Fenlason <fenlason@redhat.com> - 1.13-2
- Use macros for lib and include directories, and include dist tag in
  release field.
- Corrected License field.
- Corrected Requires lines for libuuid.
- Add Exclusive-arch x86_64
  Related: rhbz570274

* Tue May 11 2010 Mitko Haralanov <mitko@qlogic.com> - 1.13-1
- Initial build.

