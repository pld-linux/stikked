Summary:	Stikked is an Open-Source PHP Pastebin
Name:		stikked
Version:	0.8.6
Release:	0.9
License:	CC0
Group:		Applications/WWW
Source0:	https://github.com/claudehohl/Stikked/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0340e32c5a07cb8d1faefe7110309905
Source1:	apache.conf
Source2:	lighttpd.conf
Patch0:		config.patch
URL:		https://github.com/claudehohl/Stikked
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	webserver(expires)
Suggests:	webserver(rewrite)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Stikked is an Open-Source PHP Pastebin, with the aim of keeping a
simple and easy to use user interface.

%prep
%setup -q -n Stikked-%{version}
%undos -f php

# access restricted by webserver config
rm htdocs/application/config/index.html
rm htdocs/application/cache/index.html
rm htdocs/application/controllers/index.html
rm htdocs/application/core/index.html
rm htdocs/application/errors/index.html
rm htdocs/application/helpers/index.html
rm htdocs/application/hooks/index.html
rm htdocs/application/index.html
rm htdocs/application/libraries/index.html
rm htdocs/application/logs/index.html
rm htdocs/application/models/index.html
rm htdocs/application/third_party/index.html

# this is to simplify install
mv htdocs/application/config .
mv config/stikked.php{.dist,}

%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a htdocs/* $RPM_BUILD_ROOT%{_appdir}
cp -a config/* $RPM_BUILD_ROOT%{_sysconfdir}
ln -s %{_sysconfdir} $RPM_BUILD_ROOT%{_appdir}/application/config

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md AUTHORS.md CC0 doc
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
