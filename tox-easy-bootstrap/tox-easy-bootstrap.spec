%if 0%{?centos} == 7 || 0%{?fedora} >= 15 || 0%{?suse_version} >= 1210
%define with_systemd 1
%define preset_priority 80
%endif

Name:          tox-easy-bootstrap
Version:       0.0.4
Release:       1
BuildArch:     noarch
Summary:       Simple util to create and update tox-bootstrapd.conf
Group:         Applications/Internet
License:       BSD-2-Clause
URL:           https://github.com/abbat/tox.pkg/tree/master/tox-easy-bootstrap
Requires:      cron, python >= 2.6, tox-bootstrapd
BuildRequires: python-devel >= 2.6
Source0:       https://build.opensuse.org/source/home:antonbatenev:tox/%{name}/%{name}_%{version}.tar.bz2
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%if 0%{?suse_version}
BuildRequires: fdupes
BuildRequires:  -post-build-checks
%endif

%if 0%{?with_systemd}
BuildRequires:  systemd
%if 0%{?suse_version}
BuildRequires:  systemd-rpm-macros
%endif
%{?systemd_requires}
%endif

%description
Simple util to create and update tox-bootstrapd.conf with public online and private node list and restart service if needed.


%prep
%setup -q -n %{name}


%build


%install

install -d %{buildroot}%{_bindir}

install -D -m0644 %{name}.conf  %{buildroot}%{_sysconfdir}/%{name}.conf
install -D -m0644 debian/cron.d %{buildroot}%{_sysconfdir}/cron.d/%{name}
install -D -m0755 %{name}.py    %{buildroot}%{python_sitelib}/%{name}.py

ln -s %{python_sitelib}/%{name}.py %{buildroot}%{_bindir}/%{name}

%if 0%{?suse_version}
%py_compile -O %{buildroot}%{python_sitelib}
%fdupes %{buildroot}%{python_sitelib}
%endif

%if 0%{?with_systemd}
install -D -m 0644 %{name}.preset %{buildroot}%{_presetdir}/%{preset_priority}-%{name}.preset
%endif


%clean
rm -rf %{buildroot}


%post
%if 0%{?with_systemd}
systemctl preset %{name}.preset
%endif
%{_bindir}/%{name} --auto_restart=true || :


%files
%defattr(-,root,root,-)
%doc debian/copyright

%if 0%{?suse_version}
%if 0%{?with_systemd}
%{_presetdir}
%endif
%{_sysconfdir}/cron.d
%endif

%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/cron.d/%{name}

%if 0%{?with_systemd}
%{_presetdir}/%{preset_priority}-%{name}.preset
%endif

%{_bindir}/%{name}
%{python_sitelib}/%{name}.py*


%changelog
* Tue Mar 29 2016 Anthony Bilinski <me@abilinski.com> 0.0.4-1
- Initial RPM release
