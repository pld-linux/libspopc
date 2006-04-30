Summary:	simple-to-use POP3 client library
Summary(pl):	³atwa w u¿ycia biblioteka klienta POP3
Name:		libspopc
Version:	0.7.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://brouits.free.fr/libspopc/releases/%{name}-%{version}.tar.gz
# Source0-md5:	8031d23b25f60dafbdce82d60d2facb4
Source1:	http://brouits.free.fr/libspopc/try_autogen.tgz
# Source1-md5:	f63f8a26294e5b9f21d78275ff99ec55
URL:		http://brouits.free.fr/libspopc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libspopc is a simple-to-use POP3 client library. It's primary goal is
to provide an easy and quick way to host a POP3 client within a
program to C developers without exposing them to socket programming.
However, the socket layer is also accessible. libspopc allows mail
programs to connect to many POP accounts and manage email. It
implements the client side of RFC 1939. The email client can download
email headers before downloading the entire message.

%description -l pl
libspopc jest ³atw± w u¿yciu bibliotek± klienck± POP3. Jej podstawowym
zadaniem jest dostarczenie ³atwego i szybkiego w u¿yciu sposobu do
zaimplementowania klienta POP3 bez potrzeby nauki programowania gniazd
sieciowych. Warstwa gniazd jest tak¿e dostêpna. libspopc umo¿liwia
programom ³±czenie siê z wieloma kontami POP i zarz±dzanie poczt±.
Implementacja jest zgodna z RFC 1939. Klient mo¿e ¶ci±gn±æ nag³ówki
wiadomo¶ci przed ¶ci±gniêciem jej tre¶ci.

%package devel
Summary:	Header files for libspopc library
Summary(pl):	Pliki nag³ówkowe biblioteki libspopc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libspopc library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libspopc.

%package static
Summary:	Static libspopc library
Summary(pl):	Statyczna biblioteka libspopc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libspopc library.

%description static -l pl
Statyczna biblioteka libspopc.

%prep
%setup -q -a1
cp -Rf try_autogen/* .

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_includedir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{name}.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/%{name}.h
%{_libdir}/lib*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
