%global _project    tox
%global _prefix     /usr/%{_project}
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include

Summary:        Digital VCR and streaming server
Name:           %{_project}-ffmpeg
Version:        2.8.4
Release:        1
License:        GPL-3
Group:          System/Libraries
URL:            http://ffmpeg.org/
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  yasm

%description
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This version enable more support about codecs, require PostInstaller repo enable.


%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       ffmpeg-devel = %{version}-%{release}

%description    devel
FFmpeg is a complete and free Internet live audio and video
broadcasting solution for Linux/Unix. It also includes a digital
VCR. It can encode in real time in many formats including MPEG1 audio
and video, MPEG4, h263, ac3, asf, avi, real, mjpeg, and flash.
This package contains development files for %{name}


%define debug_package %{nil}


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix}                 \
    --libdir=%{_libdir}                 \
    --shlibdir=%{_libdir}               \
    --incdir=%{_includedir}             \
    --pkgconfigdir=%{_libdir}/pkgconfig \
    --disable-programs                  \
    --disable-doc                       \
    --enable-gpl                        \
    --enable-nonfree                    \
    --enable-pic

V=1 make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc README.md


%files devel
%defattr(-,root,root,-)
%doc MAINTAINERS

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_libdir}
%{_includedir}


%changelog
* Tue Dec 29 2015 Anton Batenev <antonbatenev@yandex.ru> - 2.8.4-1
- Initial
