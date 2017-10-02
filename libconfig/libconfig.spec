%global _project    tox
%global _prefix     /usr
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include
%global _datadir    %{_prefix}/share

Summary:        C/C++ configuration file library
Name:           libconfig
Version:        1.5
Release:        1
License:        LGPLv2+
Group:          System/Libraries
URL:            http://www.hyperrealm.com/libconfig/
Source0:        https://build.opensuse.org/source/home:qTox:libconfig/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  bison, flex, gcc-c++

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
%{_libdir}
%{_includedir}
%{_datadir}


%changelog
* Thu Jun 2 2016 Anthony Bilinski <me@abilinski.com> - 1.5-1
- Initial
