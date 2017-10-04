#
# spec file for package libsodium
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
%global debug_package %{nil}

%define lname libsodium18
Name:           libsodium
Version:        1.0.13
Release:        0
Summary:        Portable NaCl-based crypto library
License:        ISC
Group:          System/Libraries
Url:            https://github.com/jedisct1/libsodium
Source:         https://build.opensuse.org/source/home:qTox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
NaCl (pronounced "salt") is a new easy-to-use high-speed software library
for network communication, encryption, decryption, signatures, etc.NaCl's goal
is to provide all of the core operations needed to build higher-level cryptographic tools.

Sodium is a portable, cross-compilable, installable, packageable fork of NaCl,
with a compatible API.

%package -n  %{lname}
Summary:        Portable NaCl-based crypto library
Group:          System/Libraries

%description -n %{lname}
NaCl (pronounced "salt") is a new easy-to-use high-speed software library
for network communication, encryption, decryption, signatures, etc. NaCl's goal
is to provide all of the core operations needed to build higher-level cryptographic tools.

Sodium is a portable, cross-compilable, installable, packageable fork of NaCl,
with a compatible API.

%package devel
Summary:        Portable NaCl-based crypto library
Group:          Development/Libraries/C and C++
Requires:       %{lname} = %{version}

%description devel
This package contains all necessary include files and libraries needed
to compile and develop applications that use libsodium.

%prep
%setup -q

%build

#%if 0%{?suse_version} > 1320
#%ifarch %{ix86} x86_64
#export CFLAGS="%{optflags} -flto"
#export LDFLAGS="-flto"
#%endif
#%endif

%configure --disable-shared
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post -n %{lname} -p /sbin/ldconfig

%postun -n %{lname} -p /sbin/ldconfig

%files -n %{lname}
%defattr(0644,root,root,0755)
%{_libdir}/libsodium.a
%{_libdir}/pkgconfig/libsodium.pc

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog LICENSE README.markdown THANKS
%{_includedir}/sodium.h
%{_includedir}/sodium

%changelog
* Tue Aug 29 2017 Anthony Bilinski <me@abilinski.com> - 1.0.13-1
- Initial
