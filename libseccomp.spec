#
# Conditional build:
%bcond_without	tests		# "make check"
%bcond_without	static_libs	# static library
%bcond_without	python		# Python bindings

%ifnarch %{x8664}
# tests seem broken on x86 and x32
%undefine	with_tests
%endif
Summary:	Enhanced Seccomp (mode 2) Helper library
Summary(pl.UTF-8):	Rozszerzona biblioteka pomocnicza Seccomp (trybu 2)
Name:		libseccomp
Version:	2.2.3
Release:	2
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/seccomp/libseccomp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7db418d35d7a6168400bf6b05502f8bf
URL:		https://github.com/seccomp/libseccomp
BuildRequires:	pkgconfig
%if %{with python}
BuildRequires:	python-Cython >= 0.16
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
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

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_python:--enable-python} \
	%{!?with_static_libs:--disable-static}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config file
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libseccomp.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG CREDITS README
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

%if %{with python}
%files -n python-seccomp
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/seccomp.so
%{py_sitedir}/seccomp-%{version}-py*.egg-info
%endif
