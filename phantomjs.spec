Summary: PhantomJS is a headless WebKit with JavaScript API
Name: phantomjs
Version: 1.9.8
Release: 1%{?dist}
License: BSD
Group: unknown
URL: https://phantomjs.googlecode.com/files/
Source0: %{name}-%{version}-source.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python
BuildRequires: chrpath

%description
PhantomJS is a headless WebKit with JavaScript API. It has fast
and native support for various web standards: DOM handling,
CSS selector, JSON, Canvas, and SVG.
PhantomJS is created by Ariya Hidayat.

%prep
%setup -q

%build

./build.sh --confirm --jobs "`grep "^processor" /proc/cpuinfo | wc -l`"

/usr/bin/chrpath -d bin/%{name}

%install
rm -rf %{buildroot}
%{__install} -p -D -m 0755 bin/%{name} %{buildroot}/%{_bindir}/phantomjs

mkdir -p %{buildroot}/%{_prefix}/shared/%{name}/examples
cp examples/* %{buildroot}/%{_prefix}/shared/%{name}/examples/
cp CONTRIBUTING.md %{buildroot}/%{_prefix}/shared/%{name}
cp ChangeLog %{buildroot}/%{_prefix}/shared/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(0444,root,root)
%attr(0555,root,root)%{_bindir}/%{name}
%{_prefix}/shared/%{name}/ChangeLog
%{_prefix}/shared/%{name}/CONTRIBUTING.md
%{_prefix}/shared/%{name}/examples/


%changelog
* Thu Nov 13 2014 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.9.8-1
- Updated to PhantomJS 1.9.8.

Git Commit ID: 41f9463d5a1f6f4d443d5234054d43387499130a

* Thu Apr 10 2014 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.9.7-1
- Updated to PhantomJS 1.9.7.

Git Commit ID: f661dfc61f18d2bf20fece9ec64826ca37dc0e33

* Wed Oct 30 2013 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.9.2-1
- Updated to PhantomJS 1.9.2.

* Fri Aug 23 2013 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.9.1-1
- Updated to PhantomJS 1.9.1.

* Fri Jan 04 2013 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.6.0-2
- Updated to PhantomJS 1.6.0.

* Wed Jan 03 2013 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.5.0-2
- Fixed RPATH issues by using chrpath to make RPATH pointing relative to 
  ../lib/phantomjs (which contains the dynamically linked Qt library).
- Removed ld.so.conf.d/0-phantomjs-qt-%{_arch}.conf, it's no longer necessary.
- Changed path to PhantomJS' own Qt library from /usr/libXX/phantomjs-qt to 
  /usr/lib*/phantomjs

* Wed Apr 18 2012 Simon Josi <me@yokto.net> - 1.5.0-1
: Package PhantomJS 1.5.0.
