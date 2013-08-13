# TODO
# - figure out license and redistribution terms
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	libspotify C API
Name:		libspotify
Version:	12.1.51
Release:	1
License:	?
Group:		Libraries
Source0:	https://developer.spotify.com/download/libspotify/%{name}-%{version}-Linux-i686-release.tar.gz
# NoSource0-md5:	04735b890da0b1fc7f1f14e68a5293de
NoSource:	0
Source1:	https://developer.spotify.com/download/libspotify/%{name}-%{version}-Linux-x86_64-release.tar.gz
# NoSource1-md5:	83efddcc195d6ff12b24c97c767a5e45
NoSource:	1
Patch0:		DESTDIR.patch
URL:		https://developer.spotify.com/technologies/libspotify/
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libspotify C API package allows third-party developers to write
applications that utilize the Spotify music streaming service.

%package common
Summary:	Common files for %{name} library
Summary(pl.UTF-8):	Wspólne pliki biblioteki %{name}
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description common
Common files for %{name} library.

%description common -l pl.UTF-8
Wspólne pliki biblioteki %{name}.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%package apidocs
Summary:	%{name} API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation

%description apidocs
API and internal documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%prep
%ifarch %{ix86}
%setup -q -n %{name}-%{version}-Linux-i686-release
%endif
%ifarch %{x8664}
%setup -q -n %{name}-%{version}-Linux-x86_64-release
%endif
%patch0 -p1

install -d man
mv share/doc/libspotify/examples .
mv share/man3 man

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}
%{__make} install \
	prefix=%{_prefix} \
	lib=%{_lib} \
	ldconfig=true \
	DESTDIR=$RPM_BUILD_ROOT

cp -a man/* $RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README ChangeLog LICENSE
%attr(755,root,root) %{_libdir}/libspotify.so.*.*.*
%ghost %{_libdir}/libspotify.so.12

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc
%{_mandir}/man3/*.3spotify*

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc share/doc/libspotify/*
%endif
