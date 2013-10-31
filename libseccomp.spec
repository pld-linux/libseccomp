Summary:	Enhanced Seccomp (mode 2) Helper library
Summary(pl.UTF-8):	Rozszerzona biblioteka pomocnicza Seccomp (trybu 2)
Name:		libseccomp
Version:	2.1.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libseccomp/%{name}-%{version}.tar.gz
# Source0-md5:	1f41207b29e66a7e5e375dd48a64de85
Patch0:		%{name}-pc.patch
URL:		http://libseccomp.sourceforge.net/
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
jądra Linuksa - seccomp. API libseccomp jest zaprojektowane tak,
żeby wyabstrahować język filtrowania wywołań BPF niższego poziomu i
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

%prep
%setup -q
%patch0 -p1

%build
# not autoconf configure
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}

GCC="%{__cc}" \
CFLAGS="%{rpmcflags} -Wall" \
%{__make} \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install src/libseccomp.a $RPM_BUILD_ROOT%{_libdir}

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

%files static
%defattr(644,root,root,755)
%{_libdir}/libseccomp.a
