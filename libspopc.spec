Summary:	simple-to-use POP3 client library
Summary(pl.UTF-8):	łatwa w użycia biblioteka klienta POP3
Name:		libspopc
Version:	0.12
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://brouits.free.fr/libspopc/releases/%{name}-%{version}.tar.gz
# Source0-md5:	82a9fad896450fa4a95831f614cbd959
URL:		http://brouits.free.fr/libspopc/
BuildRequires:	openssl-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libspopc is a simple-to-use POP3 client library. It's primary goal is
to provide an easy and quick way to host a POP3 client within a
program to C developers without exposing them to socket programming.
However, the socket layer is also accessible. libspopc allows mail
programs to connect to many POP accounts and manage email. It
implements the client side of RFC 1939. The email client can download
email headers before downloading the entire message.

%description -l pl.UTF-8
libspopc jest łatwą w użyciu biblioteką kliencką POP3. Jej podstawowym
zadaniem jest dostarczenie łatwego i szybkiego w użyciu sposobu do
zaimplementowania klienta POP3 bez potrzeby nauki programowania gniazd
sieciowych. Warstwa gniazd jest także dostępna. libspopc umożliwia
programom łączenie się z wieloma kontami POP i zarządzanie pocztą.
Implementacja jest zgodna z RFC 1939. Klient może ściągnąć nagłówki
wiadomości przed ściągnięciem jej treści.

%package devel
Summary:	Header files for libspopc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libspopc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libspopc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libspopc.

%package static
Summary:	Static libspopc library
Summary(pl.UTF-8):	Statyczna biblioteka libspopc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libspopc library.

%description static -l pl.UTF-8
Statyczna biblioteka libspopc.

%prep
%setup -q
cat <<EOF > Makefile.pld
CC=%{__cc}
CFLAGS=%{rpmcflags} %{rpmcppflags} -Wall -Wextra -pedantic -pipe -fPIC -DUSE_SSL -D_REENTRANT -DUSE_SEM
LDFLAGS=%{rpmldflags}
LIBS=-lssl -lcrypto -lrt -pthread
OBJECTS=session.o queries.o parsing.o format.o objects.o libspopc.o mutex.o

all: libspopc.a libspopc.so.0.12.0

%.o : %.c libspopc.h
	\$(CC) \$(CFLAGS) -c \$<

libspopc.a : \$(OBJECTS)
	\$(RM) libspopc*.a
	ar r libspopc.a \$(OBJECTS)
	ranlib libspopc.a

libspopc.so.0.12.0 : \$(OBJECTS)
	\$(RM) libspopc*.so*
	\$(CC) -o libspopc.so.0.12.0 -shared \$(LDFLAGS) -Wl,-soname,libspopc.so.0 \$(OBJECTS) \$(LIBS)

install :
	install libspopc.a \$(DESTDIR)/%{_libdir}
	install libspopc.so.0.12.0 \$(DESTDIR)/%{_libdir}
	ln -sf libspopc.so.0.12.0 \$(DESTDIR)/%{_libdir}/libspopc.so.0
	ln -sf libspopc.so.0.12.0 \$(DESTDIR)/%{_libdir}/libspopc.so
	install libspopc.h \$(DESTDIR)/usr/include/
EOF

sed -i -e 's|\.\./libspopc\.h|libspopc.h|' examples/*.c

%build
%{__make} -f Makefile.pld

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT -f Makefile.pld

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{_libdir}/libspopc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspopc.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspopc.so
%{_includedir}/libspopc.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libspopc.a
