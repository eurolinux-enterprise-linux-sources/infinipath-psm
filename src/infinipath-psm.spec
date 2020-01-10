Summary: QLogic PSM Libraries
Name: infinipath-psm
Version: 3.2
Release: 2_ga8c3e3e_open
Epoch: 4
License: GPL
Group: System Environment/Libraries
URL: http://www.qlogic.com/
Source0: %{name}-%{version}-%{release}.tar.gz
Prefix: /usr
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Conflicts: infinipath-libs

%package devel
Summary: Development files for QLogic PSM
Group: System Environment/Development
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
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
%setup -q -n infinipath-psm-%{version}-%{release}

%build
%{__make} USE_PSM_UUID=1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
%{__make} install

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
/usr/lib64/libpsm_infinipath.so.*
/usr/lib64/libinfinipath.so.*

%files devel
%defattr(-,root,root,-)
/usr/lib64/libpsm_infinipath.so
/usr/lib64/libinfinipath.so
/usr/include/psm.h
/usr/include/psm_mq.h


%changelog
* Tue May 11 2010 Mitko Haralanov <mitko@qlogic.com> - 3.2-1
- Initial build.

