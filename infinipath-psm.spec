# infinipath-psm-2.9
Summary: QLogic PSM Libraries
Name: infinipath-psm
Version: 3.3
Release: 0.4.git6f42cdb_open%{?dist}
License: BSD or GPLv2
ExclusiveArch: x86_64
Group: System Environment/Libraries
#URL: git://git.qlogic.com/InfiniPath-PSM
Source: https://www.openfabrics.org/downloads/infinipath-psm/%{name}-%{version}-2_g6f42cdb_open.tar.gz
Source1: ipath.rules
Patch0: infinipath-psm-1.13-execstack.patch
Prefix: /usr
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: libuuid >= 2.17.2-12.7.el6
BuildRequires: libuuid-devel >= 2.17.2-12.7.el6, valgrind-devel
Conflicts: infinipath-libs

%package devel
Summary: Development files for QLogic PSM
Group: System Environment/Development
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: libuuid-devel >= 2.17.2-12.7.el6
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
%setup -q -n %{name}-%{version}-2_g6f42cdb_open
%patch0 -p1 -b .noexec

%build
%{__make} CFLAGS="$RPM_OPT_FLAGS -fpic -fPIC -D_GNU_SOURCE -funwind-tables -O3 -g3 -DPSM_USE_SYS_UUID -DNVALGRIND -Wno-error=format-security" LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
%{__make} install
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
* Thu Mar 12 2015 Doug Ledford <dledford@redhat.com> - 3.3-0.4.git6f42cdb_open
- Found the noexec stack issue, had to revive an old patch
- Related: bz1138643

* Thu Mar 12 2015 Doug Ledford <dledford@redhat.com> - 3.3-0.3.git6f42cdb_open
- Another stab at fixing up the security options
- Related: bz1138643

* Thu Mar 12 2015 Doug Ledford <dledford@redhat.com> - 3.3-0.2.git6f42cdb_open
- Fix the build so that security options are honored (found by rpmdiff)
- Related: bz1138643

* Wed Mar 11 2015 Doug Ledford <dledford@redhat.com> - 3.3-0.1.git6f42cdb_open
- Update to latest upstream
- Resolves: bz1138643

* Thu Jan 24 2013 Jay Fenlason <fenlason@redhat.com>
- Put the udev rules file in the right place
  Resolves: rhbz866732
- include a patch from upstream to fix undefined references
  Resolves: rhbz887730

* Tue Sep 25 2012 Jay Fenlason <fenlason@redhat.com> - 3.0.1-115.1015_open.1
- New upstream releas
  Resolves: rhbz818789

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

