# infinipath-psm
Summary: QLogic PSM Libraries
Name: infinipath-psm
Version: 3.2
Release: 2_ga8c3e3e_open.2%{?dist}
License: BSD or GPLv2
ExclusiveArch: x86_64
Group: System Environment/Libraries
URL: http://www.openfabrics.org/downloads/infinipath-psm/infinipath-psm-3.2-2_ga8c3e3e_open.tar.gz
Source0: infinipath-psm-3.2-2_ga8c3e3e_open.tar.gz
Source1: ipath.rules
Patch0: infinipath-psm-3.2-build.patch
Patch1: infinipath-psm-warnings.patch
Prefix: /usr
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: libuuid >= 2.17.2-3.el6
Conflicts: infinipath-libs

%package devel
Summary: Development files for QLogic PSM
Group: System Environment/Development
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: libuuid-devel >= 2.17.2-3.el6
Conflicts: infinipath-devel

%description
The PSM Messaging API, or PSM API, is QLogic's low-level
user-level communications interface for the Truescale
family of products. PSM users are enabled with mechanisms
necessary to implement higher level communications
interfaces in parallel environments.

%description devel
Development files for the libpsm_infinipath library

%prep
%setup -q -n infinipath-psm-3.2-2_ga8c3e3e_open
%patch0 -p1 -b .build
%patch1 -p1 -b .warnings

%build
make XCFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
make install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-ipath.rules

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_sysconfdir}/udev/rules.d/60-ipath.rules
%{_libdir}/libpsm_infinipath.so.*
%{_libdir}/libinfinipath.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libpsm_infinipath.so
%{_libdir}/libinfinipath.so
%{_includedir}/psm.h
%{_includedir}/psm_mq.h


%changelog
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

