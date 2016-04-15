%global _project    tox
%global _prefix     /usr/%{_project}
%global _bindir     %{_prefix}/bin
%global _libdir     %{_prefix}/lib
%global _includedir %{_prefix}/include

Summary:        SQLCipher library
Name:           %{_project}-sqlcipher
Version:        3.4.0
Release:        1
License:        BSD
Group:          System/Libraries
URL:            http://sqlcipher.net
Source0:        https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.orig.tar.bz2
BuildRequires:  openssl-devel, readline-devel, tcl-devel

%description
SQLCipher is a C library that implements an encryption in the SQLite 3
database engine.  Programs that link with the SQLCipher library can have SQL
database access without running a separate RDBMS process. It allows one to
have per-database or page-by-page encryption using AES-256 from OpenSSL.


%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries/C and C++
Requires:       %{name} = %{version}-%{release}
Provides:       sqlcipher-devel = %{version}-%{release}

%description    devel
SQLCipher is a C library that implements an encryption in the SQLite 3
database engine.  Programs that link with the SQLCipher library can have SQL
database access without running a separate RDBMS process. It allows one to
have per-database or page-by-page encryption using AES-256 from OpenSSL.


%define debug_package %{nil}


%prep
%setup -q


%build

# http://www.sqlite.org/compile.html
USER_CFLAGS="${RPM_OPT_FLAGS} -fPIC  \
    -DSQLITE_HAS_CODEC               \
    -DSQLITE_DEFAULT_AUTOVACUUM=2    \
    -DSQLITE_DEFAULT_FOREIGN_KEYS=1  \
    -DSQLITE_DEFAULT_PAGE_SIZE=32768 \
    -DSQLITE_ENABLE_STAT4            \
    -I."

USER_LDFLAGS="${RPM_LD_FLAGS} -lcrypto"

./configure \
    --prefix=%{_prefix}       \
    --disable-shared          \
    --enable-tempstore=yes    \
    --disable-tcl             \
    CFLAGS="${USER_CFLAGS}"   \
    LDFLAGS="${USER_LDFLAGS}"

make %{?_smp_mflags}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%install
make install DESTDIR=%{buildroot}

%if 0%{?suse_version}
export NO_BRP_CHECK_RPATH="true"
%endif


%files
%defattr(-,root,root,-)
%doc LICENSE README.md CHANGELOG.md

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_bindir}


%files devel
%defattr(-,root,root,-)

%if 0%{?suse_version}
%dir %{_prefix}
%endif

%{_libdir}
%{_includedir}


%changelog
* Fri Apr 15 2015 Anton Batenev <antonbatenev@yandex.ru> - 3.4.0-1
- Initial
