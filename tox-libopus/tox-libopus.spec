%global _project    tox
%global _prefix     /usr/%{_project}
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include
%global _datadir    %{_prefix}/share

Summary:        Opus codec runtime library
Name:           %{_project}-libopus
Version:        1.1.1
Release:        1
License:        BSD
Group:          System/Libraries
URL:            https://www.opus-codec.org
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  yasm

%description
Opus codec runtime library
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec.


%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}

%description    devel
Opus codec runtime library
The Opus codec is designed for interactive speech and audio transmission over
the Internet. It is designed by the IETF Codec Working Group and incorporates
technology from Skype's SILK codec and Xiph.Org's CELT codec.


%define debug_package %{nil}


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix}       \
    --disable-silent-rules    \
    --disable-maintainer-mode \
    --disable-shared          \
    --disable-doc             \
    --disable-extra-programs  \
    CFLAGS="-fPIC"

make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README


%files devel
%defattr(-,root,root,-)

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_libdir}
%{_includedir}
%{_datadir}


%changelog
* Tue Dec 1 2015 Anton Batenev <antonbatenev@yandex.ru> - 1.1.1-1
- Initial
