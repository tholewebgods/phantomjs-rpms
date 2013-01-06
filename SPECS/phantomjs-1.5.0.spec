Summary: PhantomJS is a headless WebKit with JavaScript API
Name: phantomjs
Version: 1.5.0
Release: 2%{?dist}
License: BSD
Group: unknown
URL: http://code.google.com/p/phantomjs/
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

./build.sh --jobs "`grep "^processor" /proc/cpuinfo | wc -l`"

# get path to library relative to bin directory using Python
LD_REL="$( /usr/bin/python -c "import os.path; print os.path.relpath('%{_libdir}/phantomjs', '%{_bindir}')" )"

# use chrpath to replace RPATH: <RPATH> <BINARY>
/usr/bin/chrpath -r "\$ORIGIN/${LD_REL}" bin/phantomjs 
/usr/bin/chrpath -d src/qt/lib/*.so*

%install
rm -rf %{buildroot}
%{__install} -p -D -m 0755 bin/phantomjs %{buildroot}%{_bindir}/phantomjs
mkdir -p %{buildroot}%{_libdir}/phantomjs
cp -a src/qt/lib/* %{buildroot}%{_libdir}/phantomjs
rm -rf %{buildroot}%{_libdir}/phantomjs/{fonts,pkgconfig,*.la,*.prl,README}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/phantomjs
%{_libdir}/phantomjs

%changelog
* Fri Jan 04 2013 Thomas Lehmann <t.lehmann@strato-rz.de> - 1.5.0-2
- Fixed RPATH issues by using chrpath to make RPATH pointing relative to 
  ../lib/phantomjs (which contains the dynamically linked Qt library).
- Removed ld.so.conf.d/0-phantomjs-qt-%{_arch}.conf, it's no longer necessary.
- Changed path to PhantomJS' own Qt library from /usr/libXX/phantomjs-qt to 
  /usr/lib*/phantomjs

* Wed Apr 18 2012 Simon Josi <me@yokto.net> - 1.5.0-1
- Package PhantomJS 1.5.0.

