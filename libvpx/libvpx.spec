%global _project    tox
%global _prefix     /usr/%{_project}
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include

Summary:        VP8 and VP9 video codec
Name:           %{_project}-libvpx
Version:        1.6.1
Release:        1
License:        BSD
Group:          System/Libraries
URL:            http://www.webmproject.org
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  yasm

%description
VP8 and VP9 are open video codecs, originally developed by On2 and released
as open source by Google Inc. They are the successor of the VP3 codec,
on which the Theora codec was based.


%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       libvpx-devel = %{version}-%{release}

%description    devel
VP8 and VP9 are open video codecs, originally developed by On2 and released
as open source by Google Inc. They are the successor of the VP3 codec,
on which the Theora codec was based.


%define debug_package %{nil}


%prep
%setup -q


%build
./configure \
    --prefix=%{_prefix}             \
    --enable-pic                    \
    --enable-vp8                    \
    --enable-vp9                    \
    --enable-postproc               \
    --enable-vp9-postproc           \
    --enable-runtime-cpu-detect     \
    --enable-multi-res-encoding     \
    --enable-vp9-temporal-denoising \
    --disable-unit-tests            \
    --disable-docs                  \
    --disable-examples              \
    --disable-install-docs          \
    --disable-install-srcs          \
    --extra-cflags="-fvisibility=hidden"

V=1 make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE PATENTS README


%files devel
%defattr(-,root,root,-)

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_libdir}
%{_includedir}


%changelog
* Tue Jan 24 2017 Anthony Bilinski <me@abilinski.com> - 1.6.1-1
- Initial
