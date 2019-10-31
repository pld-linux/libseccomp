#
# Conditional build:
%bcond_without	tests		# "make check"
%bcond_without	static_libs	# static library
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%ifnarch %{x8664}
# tests seem broken on x86 and x32
%undefine	with_tests
%endif
Summary:	Enhanced Seccomp (mode 2) Helper library
Summary(pl.UTF-8):	Rozszerzona biblioteka pomocnicza Seccomp (trybu 2)
Name:		libseccomp
Version:	2.4.1
Release:	3
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/seccomp/libseccomp/releases
Source0:	https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4fa6b0f39b48b8644415d7a9a9dfe9f4
URL:		https://github.com/seccomp/libseccomp
BuildRequires:	pkgconfig
%if %{with python2}
BuildRequires:	python-Cython >= 0.16
BuildRequires:	python-devel
%endif
%if %{with python3}
BuildRequires:	python3-Cython >= 0.16
BuildRequires:	python3-devel
%endif
%if %{with python2} || %{with python3}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libseccomp library provides and easy to use, platform independent,
interface to the Linux Kernel's syscall filtering mechanism: seccomp.
The libseccomp API is designed to abstract away the underlying BPF
based syscall filter language and present a more conventional
function-call based filtering interface that should be familiar to,
and easily adopted by application developers.

%description -l pl.UTF-8
Biblioteka libseccomp udostępnia łatwy w użyciu, niezależny od
platformy interfejs do mechanizmu filtrowania wywołań systemowych
jądra Linuksa - seccomp. API libseccomp jest zaprojektowane tak, żeby
wyabstrahować język filtrowania wywołań BPF niższego poziomu i
zaprezentować bardziej konwencjonalny interfejs filtrowania w oparciu
o wywołania funkcji, który powinien być bardziej przyjazny i łatwiej
adaptowalny dla programistów aplikacji.

%package devel
Summary:	Header files for Seccomp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Seccomp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Seccomp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Seccomp.

%package static
Summary:	Static Seccomp library
Summary(pl.UTF-8):	Statyczna biblioteka Seccomp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Seccomp library.

%description static -l pl.UTF-8
Statyczna biblioteka Seccomp.

%package -n python-seccomp
Summary:	Python binding for seccomp library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki seccomp
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-seccomp
Python binding for seccomp library.

%description -n python-seccomp -l pl.UTF-8
Wiązanie Pythona do biblioteki seccomp.

%package -n python3-seccomp
Summary:	Python 3 binding for seccomp library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki seccomp
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-seccomp
Python 3 binding for seccomp library.

%description -n python3-seccomp -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki seccomp.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	--disable-python
	%{!?with_static_libs:--disable-static}
%{__make}

CPPFLAGS="-I$(pwd)/include"; export CPPFLAGS
cd src/python
VERSION_RELEASE="%{version}"; export VERSION_RELEASE
%if %{with python2}
%py_build
#%{?with_tests:test}
%endif

%if %{with python3}
%py3_build
#%{?with_tests:test}
%endif
cd ../../

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libseccomp.la

CPPFLAGS="-I$(pwd)/include"; export CPPFLAGS
cd src/python
VERSION_RELEASE="%{version}"; export VERSION_RELEASE
%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS README.md
%attr(755,root,root) %{_bindir}/scmp_sys_resolver
%attr(755,root,root) %{_libdir}/libseccomp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libseccomp.so.2
%{_mandir}/man1/scmp_sys_resolver.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libseccomp.so
%{_includedir}/seccomp.h
%{_pkgconfigdir}/libseccomp.pc
%{_mandir}/man3/seccomp_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libseccomp.a
%endif

%if %{with python2}
%files -n python-seccomp
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/seccomp.so
%{py_sitedir}/seccomp-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-seccomp
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/seccomp.*.so
%{py3_sitedir}/seccomp-%{version}-py*.egg-info
%endif
