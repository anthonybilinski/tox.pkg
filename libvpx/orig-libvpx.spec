#
# spec file for package libvpx
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
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


%define         soname 3

Name:           libvpx
Version:        1.5.0
Release:        0
Summary:        VP8 codec library
License:        BSD-3-Clause and GPL-2.0+
Group:          Productivity/Multimedia/Other
Url:            http://www.webmproject.org/
Source0:        http://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-%{version}.tar.bz2
Source1000:     baselibs.conf
# PATCH-FIX-UPSTREAM libvpx-define-config_pic.patch dimstar@opensuse.org -- For older compilers, CONFIG_PIC need to be defined.
Patch1:         libvpx-define-config_pic.patch
Patch2:         libvpx-configure-add-s390.patch
Patch3:         libvpx-disable-cross-for-arm.patch
Patch4:         libvpx-armv7-use-hard-float.patch
# Needed to be able to create pkgconfig() provides.
BuildRequires:  pkg-config
BuildRequires:  yasm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package -n vpx-tools
Summary:        VP8 codec library - Utilities
License:        BSD-3-Clause and GPL-2.0+
Group:          Productivity/Multimedia/Other

%description -n vpx-tools
This package contains utilities around the vp8 codec sdk.

WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package -n %{name}%{soname}

Summary:        VP8 codec library
License:        BSD-3-Clause
Group:          System/Libraries

%description -n %{name}%{soname}
WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%package devel
Summary:        VP8 codec library - Development headers
License:        BSD-3-Clause and GPL-2.0+
Group:          Development/Languages/C and C++
Requires:       %{name}%{soname} = %{version}

%description devel
Development headers and library

WebM is an open, royalty-free, media file format designed for the web.

WebM defines the file container structure, video and audio formats.
WebM files consist of video streams compressed with the VP8 video codec
and audio streams compressed with the Vorbis audio codec.
The WebM file structure is based on the Matroska container.

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
cd build
export CFLAGS="-std=gnu89 %{optflags}"
# It is only an emulation of autotools configure; the macro does not work

# libvpx default enable NEON support on ARMv7, unfortunately some ARMv7
# CPU doesn't have NEON, e.g. NVIDIA Tegra 2.
# So, we still set -mfpu=neon when build libvpx rpm, but also enable
# runtime-cpu-detect for runtime detect NEON.
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-debug \
    --enable-shared \
%ifarch armv5tel armv5el
    --target=armv5te-linux-gcc \
%endif
%ifarch armv7l armv7hl
    --target=armv7-linux-gcc \
    --enable-runtime-cpu-detect \
%endif
    --enable-pic
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%buildroot install
# Remove static library, should not be used on openSUSE to avoid efforts on
# (security) updates
rm %{buildroot}%{_libdir}/libvpx.a

%clean
rm -rf %{buildroot}

%post -n %{name}%{soname} -p /sbin/ldconfig

%postun -n %{name}%{soname} -p /sbin/ldconfig

%files -n vpx-tools
%defattr(-,root,root)
%{_bindir}/*

%files -n %{name}%{soname}
%defattr(-, root, root)
%doc LICENSE AUTHORS README CHANGELOG
%{_libdir}/libvpx.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/vpx/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%changelog

