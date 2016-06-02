%global _project    tox
%global _prefix     /usr/%{_project}
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include
%global _datadir    %{_prefix}/share

Summary:        C/C++ configuration file library
Name:           %{_project}-libconfig
Version:        1.5
Release:        1
License:        LGPLv2+
Group:          System/Libraries
URL:            http://www.hyperrealm.com/libconfig/
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox:libconfig/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  bison, flex

%description
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.


%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Provides:       libconfig-devel = %{version}-%{release}

%description    devel
Libconfig is a simple library for manipulating structured configuration
files. This file format is more compact and more readable than XML. And
unlike XML, it is type-aware, so it is not necessary to do string parsing
in application code.


%define debug_package %{nil}


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix}       \
    --disable-silent-rules    \
    --disable-shared          \
    --with-pic

make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB README


%files devel
%defattr(-,root,root,-)

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_libdir}
%{_includedir}
%{_datadir}


%changelog
* Thu Jun 2 2016 Anton Batenev <antonbatenev@yandex.ru> - 1.5-1
- Initial
