%global _project    tox
%global _prefix     /usr/%{_project}
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include

Name:           %{_project}-libsodium
Version:        1.0.13
Release:        1
Summary:        A fork of networking and cryptography library with compatible APIs
License:        ISC
Group:          System/Libraries
URL:            https://github.com/jedisct1/libsodium
BuildRequires:  pkgconfig
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Sodium is a portable, cross-compilable, installable, packageable library
forked from NaCl(networking and cryptography library), with a compatible API.
Its goal is to provide all of the core operations needed to build higher-level
cryptographic tools.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       libsodium-devel = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.


%define debug_package %{nil}


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix}         \
    --libdir=%{_libdir}         \
    --includedir=%{_includedir} \
    --disable-shared            \
    --disable-silent-rules

make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make DESTDIR=%{buildroot} install


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE README.markdown THANKS


%files devel
%defattr(-,root,root,-)
%{_prefix}


%changelog
* Tue Aug 29 2017 Anton Batenev <antonbatenev@yandex.ru> - 1.0.13-1
- Initial
