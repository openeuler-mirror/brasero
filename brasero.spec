Name:           brasero
Version:        3.12.3
Release:        1
Summary:        Brasero – CD/DVD burner
License:        GPLv3+
URL:            https://wiki.gnome.org/Apps/Brasero
Source0:        https://download.gnome.org/sources/brasero/3.12/brasero-%{version}.tar.xz

BuildRequires:  gtk3-devel >= 2.99.0 glib2-devel >= 2.15.6 gettext intltool gtk-doc desktop-file-utils
BuildRequires:  gstreamer1-devel >= 0.11.92 gstreamer1-plugins-base-devel >= 0.11.92 totem-pl-parser-devel >= 2.22.0
BuildRequires:  libnotify-devel >= 0.7.0 libxml2-devel >= 2.6.0 dbus-glib-devel >= 0.7.2 libxslt libappstream-glib
BuildRequires:  libburn-devel >= 0.4.0 libisofs-devel >= 0.6.4 nautilus-devel >= 2.22.2 libSM-devel libcanberra-devel
BuildRequires:  gobject-introspection-devel tracker-devel itstool yelp-tools
Requires:       dvd+rw-tools wodim genisoimage icedax cdrdao

Provides:       %{name}-libs = %{version}-%{release} %{name}-nautilus = %{version}-%{release}
Obsoletes:      %{name}-libs < %{version}-%{release} %{name}-nautilus < %{version}-%{release}

%description
Brasero is a GNOME application to burn CD/DVD, designed to be as simple as possible.
It has some unique features to enable users to create their discs easily and quickly.

%package        devel
Summary:        Headers for developing programs provided for brasero
Requires:       %{name} = %{version}-%{release}

%description devel
The package contains the required static libraries and header files
for developing a brasero application.

%package        help
Summary:        Help document for the brasero package

%description help
Help document for the brasero package.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --enable-nautilus --enable-libburnia --enable-search --enable-playlist \
           --enable-preview --enable-inotify --disable-caches
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build

%install
%make_install
%delete_la
%find_lang brasero

appstream-util replace-screenshots %{buildroot}%{_datadir}/metainfo/brasero.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/b.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/brasero/c.png

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/brasero.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files -f brasero.lang
%doc AUTHORS NEWS README COPYING

%{_bindir}/*
%{_libdir}/{brasero3,*.so.*,girepository-1.0/*.typelib,nautilus/extensions-3.0/*.so}

%{_datadir}/{brasero,applications/brasero.desktop,metainfo/brasero.appdata.xml}
%{_datadir}/{icons/hicolor/*/apps/*,mime/packages/*,GConf/gsettings/brasero.convert}
%{_datadir}/{glib-2.0/schemas/org.gnome.brasero.gschema.xml,applications/brasero-nautilus.desktop}

%files devel
%doc %{_datadir}/gtk-doc/html/libbrasero-media
%doc %{_datadir}/gtk-doc/html/libbrasero-burn
%doc ChangeLog
%{_libdir}/{*.so,pkgconfig/*.pc}
%{_includedir}/brasero3
%{_datadir}/gir-1.0/*.gir

%files help
%{_datadir}/help/*
%{_mandir}/man1/%{name}.*

%changelog
* Wed Apr 12 2023 liyanan <thistleslyn@163.com> - 3.12.3-1
- Update to 3.12.3

* Wed Nov 27 2019 zhangchunyu <zhangchunyu11@huawei.com> - 3.12.2-8
- Package init

