# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%global no64bit   0
%global winegecko 2.47
%global winemono  4.9.0
#global _default_patch_fuzz 2
%ifarch %{ix86} x86_64
%global wineacm acm
%global winecpl cpl
%global winedll dll
%global winedrv drv
%global wineexe exe
%global wineocx ocx
%global winesys sys
%global winetlb tlb
%else
%global wineacm acm.so
%global winecpl cpl.so
%global winedll dll.so
%global winedrv drv.so
%global wineexe exe.so
%global wineocx ocx.so
%global winesys sys.so
%global winetlb tlb.so
%endif

# build with wine-staging patches, see:  https://github.com/wine-staging/wine-staging
%if 0%{?fedora}
%global wine_staging 1
%endif # 0%{?fedora}

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

Name:           wine
Version:        4.13
Release:        2%{?dist}
Summary:        A compatibility layer for windows applications

License:        LGPLv2+
URL:            https://www.winehq.org/
Source0:        https://dl.winehq.org/wine/source/4.x/wine-%{version}.tar.xz
Source10:       https://dl.winehq.org/wine/source/4.x/wine-%{version}.tar.xz.sign

Source1:        wine.init
Source2:        wine.systemd
Source3:        wine-README-Fedora
Source4:        wine-32.conf
Source5:        wine-64.conf

# desktop files
Source100:      wine-notepad.desktop
Source101:      wine-regedit.desktop
Source102:      wine-uninstaller.desktop
Source103:      wine-winecfg.desktop
Source104:      wine-winefile.desktop
Source105:      wine-winemine.desktop
Source106:      wine-winhelp.desktop
Source107:      wine-wineboot.desktop
Source108:      wine-wordpad.desktop
Source109:      wine-oleview.desktop

# build fixes

# wine bugs

# desktop dir
Source200:      wine.menu
Source201:      wine.directory

# mime types
Source300:      wine-mime-msi.desktop


# smooth tahoma (#693180)
# disable embedded bitmaps
Source501:      wine-tahoma.conf
# and provide a readme
Source502:      wine-README-tahoma

Patch511:       wine-cjk.patch

%if 0%{?wine_staging}
# wine-staging patches
# pulseaudio-patch is covered by that patch-set, too.
Source900: https://github.com/wine-staging/wine-staging/archive/v%{version}.tar.gz#/wine-staging-%{version}.tar.gz
%endif

%if !%{?no64bit}
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
%else
ExclusiveArch:  %{ix86} %{arm}
%endif

BuildRequires:  bison
BuildRequires:  flex
%ifarch aarch64
BuildRequires:  clang >= 5.0
%else
BuildRequires:  gcc
%endif
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  autoconf
BuildRequires:  desktop-file-utils
BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  freeglut-devel
BuildRequires:  lcms2-devel
BuildRequires:  libieee1284-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libusb-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  ncurses-devel
%if 0%{?fedora}
BuildRequires:  ocl-icd-devel
BuildRequires:  opencl-headers
%endif
BuildRequires:  openldap-devel
BuildRequires:  perl-generators
BuildRequires:  unixODBC-devel
BuildRequires:  sane-backends-devel
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  fontforge freetype-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  isdn4k-utils-devel
BuildRequires:  libpcap-devel
# modular x
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel mesa-libGLU-devel mesa-libOSMesa-devel
BuildRequires:  libXxf86dga-devel libXxf86vm-devel
BuildRequires:  libXrandr-devel libXrender-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  cups-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXi-devel
BuildRequires:  libXcursor-devel
BuildRequires:  dbus-devel
BuildRequires:  gnutls-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  gsm-devel
BuildRequires:  libv4l-devel
BuildRequires:  fontpackages-devel
BuildRequires:  libtiff-devel
BuildRequires:  gettext-devel
BuildRequires:  chrpath
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
%if 0%{?fedora} > 24
BuildRequires:  mpg123-devel
%endif
BuildRequires:  SDL2-devel
BuildRequires:  libvkd3d-devel
BuildRequires:  vulkan-devel
BuildRequires:  libFAudio-devel

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  gtk3-devel
BuildRequires:  libattr-devel
BuildRequires:  libva-devel
%endif # 0%{?wine_staging}

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
BuildRequires:  openal-soft-devel
BuildRequires:  icoutils
%endif

Requires:       wine-common = %{version}-%{release}
Requires:       wine-desktop = %{version}-%{release}
Requires:       wine-fonts = %{version}-%{release}

# x86-32 parts
%ifarch %{ix86} x86_64
%if 0%{?fedora} || 0%{?rhel} <= 6
Requires:       wine-core(x86-32) = %{version}-%{release}
Requires:       wine-capi(x86-32) = %{version}-%{release}
Requires:       wine-cms(x86-32) = %{version}-%{release}
Requires:       wine-ldap(x86-32) = %{version}-%{release}
Requires:       wine-twain(x86-32) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-32) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} == 6
Requires:       wine-openal(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       wine-opencl(x86-32) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw32-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
#  wait for rhbz#968860 to require arch-specific samba-winbind-clients
Requires:       /usr/bin/ntlm_auth
Requires:       mesa-dri-drivers(x86-32)
%endif
%endif

# x86-64 parts
%ifarch x86_64
Requires:       wine-core(x86-64) = %{version}-%{release}
Requires:       wine-capi(x86-64) = %{version}-%{release}
Requires:       wine-cms(x86-64) = %{version}-%{release}
Requires:       wine-ldap(x86-64) = %{version}-%{release}
Requires:       wine-twain(x86-64) = %{version}-%{release}
Requires:       wine-pulseaudio(x86-64) = %{version}-%{release}
%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
Requires:       wine-openal(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora}
Requires:       wine-opencl(x86-64) = %{version}-%{release}
%endif
%if 0%{?fedora} >= 17
Requires:       mingw64-wine-gecko = %winegecko
Requires:       wine-mono = %winemono
%endif
Requires:       mesa-dri-drivers(x86-64)
%endif

# ARM parts
%ifarch %{arm} aarch64
Requires:       wine-core = %{version}-%{release}
Requires:       wine-capi = %{version}-%{release}
Requires:       wine-cms = %{version}-%{release}
Requires:       wine-ldap = %{version}-%{release}
Requires:       wine-twain = %{version}-%{release}
Requires:       wine-pulseaudio = %{version}-%{release}
Requires:       wine-openal = %{version}-%{release}
%if 0%{?fedora}
Requires:       wine-opencl = %{version}-%{release}
%endif
Requires:       mesa-dri-drivers
Requires:       samba-winbind-clients
%endif

# aarch64 parts
%ifarch aarch64
Requires:       wine-core(aarch-64) = %{version}-%{release}
Requires:       wine-capi(aarch-64) = %{version}-%{release}
Requires:       wine-cms(aarch-64) = %{version}-%{release}
Requires:       wine-ldap(aarch-64) = %{version}-%{release}
Requires:       wine-twain(aarch-64) = %{version}-%{release}
Requires:       wine-pulseaudio(aarch-64) = %{version}-%{release}
Requires:       wine-openal(aarch-64) = %{version}-%{release}
Requires:       wine-opencl(aarch-64) = %{version}-%{release}
Requires:       mingw64-wine-gecko = %winegecko
Requires:       mesa-dri-drivers(aarch-64)
%endif

%description
Wine as a compatibility layer for UNIX to run Windows applications. This
package includes a program loader, which allows unmodified Windows
3.x/9x/NT binaries to run on x86 and x86_64 Unixes. Wine can use native system
.dll files if they are available.

In Fedora wine is a meta-package which will install everything needed for wine
to work smoothly. Smaller setups can be achieved by installing some of the
wine-* sub packages.

%package core
Summary:        Wine core package
Requires(postun): /sbin/ldconfig
Requires(posttrans):   %{_sbindir}/alternatives
Requires(preun):       %{_sbindir}/alternatives

# require -filesystem
Requires:       wine-filesystem = %{version}-%{release}

%ifarch %{ix86}
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-32)
Requires:       freetype(x86-32)
Requires:       nss-mdns(x86-32)
Requires:       gnutls(x86-32)
Requires:       libXcomposite(x86-32)
Requires:       libXcursor(x86-32)
Requires:       libXinerama(x86-32)
Requires:       libXrandr(x86-32)
Requires:       libXrender(x86-32)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-32)
Requires:       libpcap(x86-32)
Requires:       mesa-libOSMesa(x86-32)
Requires:       libv4l(x86-32)
Requires:       unixODBC(x86-32)
Requires:       SDL2(x86-32)
Requires:       vulkan-loader(x86-32)
%if 0%{?wine_staging}
Requires:       libva(x86-32)
%endif
%endif

%ifarch x86_64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs(x86-64)
Requires:       freetype(x86-64)
Requires:       nss-mdns(x86-64)
Requires:       gnutls(x86-64)
Requires:       libXcomposite(x86-64)
Requires:       libXcursor(x86-64)
Requires:       libXinerama(x86-64)
Requires:       libXrandr(x86-64)
Requires:       libXrender(x86-64)
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng(x86-64)
Requires:       libpcap(x86-64)
Requires:       mesa-libOSMesa(x86-64)
Requires:       libv4l(x86-64)
Requires:       unixODBC(x86-64)
Requires:       SDL2(x86-64)
Requires:       vulkan-loader(x86-64)
%if 0%{?wine_staging}
Requires:       libva(x86-64)
%endif
%endif

%ifarch %{arm} aarch64
# CUPS support uses dlopen - rhbz#1367537
Requires:       cups-libs
Requires:       freetype
Requires:       nss-mdns
Requires:       gnutls
Requires:       libXrender
Requires:       libXcursor
#dlopen in windowscodesc (fixes rhbz#1085075)
Requires:       libpng
Requires:       libpcap
Requires:       mesa-libOSMesa
Requires:       libv4l
Requires:       unixODBC
Requires:       SDL2
Requires:       vulkan-loader
%if 0%{?wine_staging}
Requires:       libva
%endif
%endif

# removed as of 1.7.35
Obsoletes:      wine-wow < 1.7.35
Provides:       wine-wow = %{version}-%{release}

%description core
Wine core package includes the basic wine stuff needed by all other packages.

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%package systemd
Summary:        Systemd config for the wine binfmt handler
Requires:       systemd >= 23
BuildArch:      noarch
Requires(post):  systemd
Requires(postun): systemd
Obsoletes:      wine-sysvinit < %{version}-%{release}

%description systemd
Register the wine binary handler for windows executables via systemd binfmt
handling. See man binfmt.d for further information.
%endif

%if 0%{?rhel} == 6
%package sysvinit
Summary:        SysV initscript for the wine binfmt handler
BuildArch:      noarch
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service

%description sysvinit
Register the wine binary handler for windows executables via SysV init files.
%endif

%package filesystem
Summary:        Filesystem directories for wine
BuildArch:      noarch

%description filesystem
Filesystem directories and basic configuration for wine.

%package common
Summary:        Common files
Requires:       wine-core = %{version}-%{release}
BuildArch:      noarch

%description common
Common wine files and scripts.

%package desktop
Summary:        Desktop integration features for wine
Requires(post): desktop-file-utils >= 0.8
Requires(postun): desktop-file-utils >= 0.8
Requires:       wine-core = %{version}-%{release}
Requires:       wine-common = %{version}-%{release}
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
Requires:       wine-systemd = %{version}-%{release}
%endif
%if 0%{?rhel} == 6
Requires:       wine-sysvinit = %{version}-%{release}
%endif
Requires:       hicolor-icon-theme
BuildArch:      noarch

%description desktop
Desktop integration features for wine, including mime-types and a binary format
handler service.

%package fonts
Summary:       Wine font files
BuildArch:     noarch
# arial-fonts are available with wine-staging patchset, only.
%if 0%{?wine_staging}
Requires:      wine-arial-fonts = %{version}-%{release}
%else # 0%{?wine_staging}
Obsoletes:     wine-arial-fonts <= %{version}-%{release}
%endif # 0%{?wine_staging}
Requires:      wine-courier-fonts = %{version}-%{release}
Requires:      wine-fixedsys-fonts = %{version}-%{release}
Requires:      wine-small-fonts = %{version}-%{release}
Requires:      wine-system-fonts = %{version}-%{release}
Requires:      wine-marlett-fonts = %{version}-%{release}
Requires:      wine-ms-sans-serif-fonts = %{version}-%{release}
Requires:      wine-tahoma-fonts = %{version}-%{release}
# times-new-roman-fonts are available with wine_staging-patchset, only.
%if 0%{?wine_staging}
Requires:      wine-times-new-roman-fonts = %{version}-%{release}
%else # 0%{?wine_staging}
Obsoletes:     wine-times-new-roman-fonts <= %{version}-%{release}
Obsoletes:     wine-times-new-roman-fonts-system <= %{version}-%{release}
%endif # 0%{?wine_staging}
Requires:      wine-symbol-fonts = %{version}-%{release}
Requires:      wine-wingdings-fonts = %{version}-%{release}
# intermediate fix for #593140
Requires:      liberation-sans-fonts liberation-serif-fonts liberation-mono-fonts
%if 0%{?fedora} > 12
Requires:      liberation-narrow-fonts
%endif

%description fonts
%{summary}

%if 0%{?wine_staging}
%package arial-fonts
Summary:       Wine Arial font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description arial-fonts
%{summary}
%endif # 0%{?wine_staging}

%package courier-fonts
Summary:       Wine Courier font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description courier-fonts
%{summary}

%package fixedsys-fonts
Summary:       Wine Fixedsys font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description fixedsys-fonts
%{summary}

%package small-fonts
Summary:       Wine Small font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description small-fonts
%{summary}

%package system-fonts
Summary:       Wine System font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description system-fonts
%{summary}


%package marlett-fonts
Summary:       Wine Marlett font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description marlett-fonts
%{summary}


%package ms-sans-serif-fonts
Summary:       Wine MS Sans Serif font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description ms-sans-serif-fonts
%{summary}

# rhbz#693180
# http://lists.fedoraproject.org/pipermail/devel/2012-June/168153.html
%package tahoma-fonts
Summary:       Wine Tahoma font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description tahoma-fonts
%{summary}
Please note: If you want system integration for wine tahoma fonts install the
wine-tahoma-fonts-system package.

%package tahoma-fonts-system
Summary:       Wine Tahoma font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-tahoma-fonts = %{version}-%{release}

%description tahoma-fonts-system
%{summary}

%if 0%{?wine_staging}
%package times-new-roman-fonts
Summary:       Wine Times New Roman font family
BuildArch:     noarch
Requires:      wine-filesystem = %{version}-%{release}

%description times-new-roman-fonts
%{summary}
Please note: If you want system integration for wine times new roman fonts install the
wine-times-new-roman-fonts-system package.

%package times-new-roman-fonts-system
Summary:       Wine Times New Roman font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-times-new-roman-fonts = %{version}-%{release}

%description times-new-roman-fonts-system
%{summary}
%endif

%package symbol-fonts
Summary:       Wine Symbol font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description symbol-fonts
%{summary}

%package wingdings-fonts
Summary:       Wine Wingdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description wingdings-fonts
%{summary}
Please note: If you want system integration for wine wingdings fonts install the
wine-wingdings-fonts-system package.

%package wingdings-fonts-system
Summary:       Wine Wingdings font family system integration
BuildArch:     noarch
Requires:      fontpackages-filesystem
Requires:      wine-wingdings-fonts = %{version}-%{release}

%description wingdings-fonts-system
%{summary}


%package ldap
Summary: LDAP support for wine
Requires: wine-core = %{version}-%{release}

%description ldap
LDAP support for wine

%package cms
Summary: Color Management for wine
Requires: wine-core = %{version}-%{release}

%description cms
Color Management for wine

%package twain
Summary: Twain support for wine
Requires: wine-core = %{version}-%{release}
%ifarch %{ix86}
Requires: sane-backends-libs(x86-32)
%endif
%ifarch x86_64
Requires: sane-backends-libs(x86-64)
%endif
%ifarch %{arm} aarch64
Requires: sane-backends-libs
%endif

%description twain
Twain support for wine

%package capi
Summary: ISDN support for wine
Requires: wine-core = %{version}-%{release}
%ifarch x86_64
Requires:       isdn4k-utils(x86-64)
%endif
%ifarch %{ix86}
Requires:       isdn4k-utils(x86-32)
%endif
%ifarch %{arm} aarch64
Requires:       isdn4k-utils
%endif

%description capi
ISDN support for wine

%package devel
Summary: Wine development environment
Requires: wine-core = %{version}-%{release}

%description devel
Header, include files and library definition files for developing applications
with the Wine Windows(TM) emulation libraries.

%package pulseaudio
Summary: Pulseaudio support for wine
Requires: wine-core = %{version}-%{release}
# midi output
Requires: wine-alsa%{?_isa} = %{version}-%{release}

%description pulseaudio
This package adds a pulseaudio driver for wine.

%package alsa
Summary: Alsa support for wine
Requires: wine-core = %{version}-%{release}

%description alsa
This package adds an alsa driver for wine.

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%package openal
Summary: Openal support for wine
Requires: wine-core = %{version}-%{release}

%description openal
This package adds an openal driver for wine.
%endif

%if 0%{?fedora}
%package opencl
Summary: OpenCL support for wine
Requires: wine-core = %{version}-%{release}

%Description opencl
This package adds the opencl driver for wine.
%endif

%prep
%setup -q -n wine-%{version}
%patch511 -p1 -b.cjk

%if 0%{?wine_staging}
# setup and apply wine-staging patches
gzip -dc %{SOURCE900} | tar -xf - --strip-components=1

# Disable XAudio patchsets in favor of FAudio
patches/patchinstall.sh DESTDIR="`pwd`" --all

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

%endif # 0%{?wine_staging}

%build

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

%ifarch aarch64
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`"
%endif

%configure \
 --sysconfdir=%{_sysconfdir}/wine \
 --x-includes=%{_includedir} --x-libraries=%{_libdir} \
 --without-hal --with-dbus \
 --with-x \
%ifarch %{arm}
 --with-float-abi=hard \
%endif
%ifarch x86_64 aarch64
 --enable-win64 \
%endif
%{?wine_staging: --with-xattr} \
 --disable-tests

make %{?_smp_mflags} TARGETFLAGS=""

%install

%makeinstall \
        includedir=%{buildroot}%{_includedir} \
        sysconfdir=%{buildroot}%{_sysconfdir}/wine \
        dlldir=%{buildroot}%{_libdir}/wine \
        LDCONFIG=/bin/true \
        UPDATE_DESKTOP_DATABASE=/bin/true

# setup for alternatives usage
%ifarch x86_64 aarch64
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver64
%endif
%ifarch %{ix86} %{arm}
mv %{buildroot}%{_bindir}/wine %{buildroot}%{_bindir}/wine32
mv %{buildroot}%{_bindir}/wineserver %{buildroot}%{_bindir}/wineserver32
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
touch %{buildroot}%{_bindir}/wineserver
mv %{buildroot}%{_libdir}/wine/dxgi.dll.so %{buildroot}%{_libdir}/wine/wine-dxgi.dll.so
mv %{buildroot}%{_libdir}/wine/d3d9.%{winedll} %{buildroot}%{_libdir}/wine/wine-d3d9.%{winedll}
mv %{buildroot}%{_libdir}/wine/d3d10.%{winedll} %{buildroot}%{_libdir}/wine/wine-d3d10.%{winedll}
mv %{buildroot}%{_libdir}/wine/d3d10_1.%{winedll} %{buildroot}%{_libdir}/wine/wine-d3d10_1.%{winedll}
mv %{buildroot}%{_libdir}/wine/d3d10core.%{winedll} %{buildroot}%{_libdir}/wine/wine-d3d10core.%{winedll}
mv %{buildroot}%{_libdir}/wine/d3d11.%{winedll} %{buildroot}%{_libdir}/wine/wine-d3d11.%{winedll}
touch %{buildroot}%{_libdir}/wine/dxgi.dll.so
touch %{buildroot}%{_libdir}/wine/d3d9.%{winedll}
touch %{buildroot}%{_libdir}/wine/d3d10.%{winedll}
touch %{buildroot}%{_libdir}/wine/d3d10_1.%{winedll}
touch %{buildroot}%{_libdir}/wine/d3d10core.%{winedll}
touch %{buildroot}%{_libdir}/wine/d3d11.%{winedll}

# remove rpath
chrpath --delete %{buildroot}%{_bindir}/wmc
chrpath --delete %{buildroot}%{_bindir}/wrc
%ifarch x86_64 aarch64
chrpath --delete %{buildroot}%{_bindir}/wine64
chrpath --delete %{buildroot}%{_bindir}/wineserver64
%else
chrpath --delete %{buildroot}%{_bindir}/wine32
chrpath --delete %{buildroot}%{_bindir}/wineserver32
%endif

mkdir -p %{buildroot}%{_sysconfdir}/wine

# Allow users to launch Windows programs by just clicking on the .exe file...
%if 0%{?rhel} < 7
mkdir -p %{buildroot}%{_initrddir}
install -p -c -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/wine
%endif
%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_binfmtdir}
install -p -c -m 644 %{SOURCE2} %{buildroot}%{_binfmtdir}/wine.conf
%endif

# add wine dir to desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
install -p -m 644 %{SOURCE200} \
%{buildroot}%{_sysconfdir}/xdg/menus/applications-merged/wine.menu
mkdir -p %{buildroot}%{_datadir}/desktop-directories
install -p -m 644 %{SOURCE201} \
%{buildroot}%{_datadir}/desktop-directories/Wine.directory

# add gecko dir
mkdir -p %{buildroot}%{_datadir}/wine/gecko

# add mono dir
mkdir -p %{buildroot}%{_datadir}/wine/mono

# extract and install icons
%if 0%{?fedora} > 10
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

# This replacement masks a composite program icon .SVG down
# so that only its full-size scalable icon is visible
PROGRAM_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="368"\n'\
'   y="8"\n'\
'   viewBox="368, 8, 256, 256"/;'
MAIN_ICONFIX='s/height="272"/height="256"/;'\
's/width="632"/width="256"\n'\
'   x="8"\n'\
'   y="8"\n'\
'   viewBox="8, 8, 256, 256"/;'

# This icon file is still in the legacy format
install -p -m 644 dlls/user32/resources/oic_winlogo.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg
sed -i -e "$MAIN_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wine.svg

# The rest come from programs/, and contain larger scalable icons
# with a new layout that requires the PROGRAM_ICONFIX sed adjustment
install -p -m 644 programs/notepad/notepad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/notepad.svg

install -p -m 644 programs/regedit/regedit.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/regedit.svg

install -p -m 644 programs/msiexec/msiexec.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/msiexec.svg

install -p -m 644 programs/winecfg/winecfg.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winecfg.svg

install -p -m 644 programs/winefile/winefile.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winefile.svg

install -p -m 644 programs/winemine/winemine.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winemine.svg

install -p -m 644 programs/winhlp32/winhelp.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/winhelp.svg

install -p -m 644 programs/wordpad/wordpad.svg \
 %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg
sed -i -e "$PROGRAM_ICONFIX" %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/wordpad.svg

%endif

# install desktop files
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE100}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE101}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE102}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE103}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE104}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE105}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE106}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE107}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE108}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE109}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/wine.desktop

#mime-types
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE300}

cp -p %{SOURCE3} README-FEDORA

cp -p %{SOURCE502} README-tahoma

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/

%ifarch %{ix86} %{arm}
install -p -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif

%ifarch x86_64 aarch64
install -p -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/ld.so.conf.d/
%endif


# install Tahoma font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-tahoma-fonts
ln -s ../../wine/fonts/tahoma.ttf tahoma.ttf
ln -s ../../wine/fonts/tahomabd.ttf tahomabd.ttf
popd

# add config and readme for tahoma
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -p -m 0644 %{SOURCE501} %{buildroot}%{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf

ln -s %{_fontconfig_templatedir}/20-wine-tahoma-nobitmaps.conf \
      %{buildroot}%{_fontconfig_confdir}/20-wine-tahoma-nobitmaps.conf

%if 0%{?wine_staging}
# install Times New Roman font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-times-new-roman-fonts
ln -s ../../wine/fonts/times.ttf times.ttf
popd
%endif

# install Wingdings font for system package
install -p -m 0755 -d %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
pushd %{buildroot}/%{_datadir}/fonts/wine-wingdings-fonts
ln -s ../../wine/fonts/wingding.ttf wingding.ttf
popd

# clean readme files
pushd documentation
for lang in it hu sv es pt pt_br;
do iconv -f iso8859-1 -t utf-8 README.$lang > \
 README.$lang.conv && mv -f README.$lang.conv README.$lang
done;
popd

%if 0%{?fedora} || 0%{?rhel} > 6
rm -f %{buildroot}%{_initrddir}/wine
%endif

# wine makefiles are currently broken and don't install the wine man page
install -p -m 0644 loader/wine.man %{buildroot}%{_mandir}/man1/wine.1
install -p -m 0644 loader/wine.de.UTF-8.man %{buildroot}%{_mandir}/de.UTF-8/man1/wine.1
install -p -m 0644 loader/wine.fr.UTF-8.man %{buildroot}%{_mandir}/fr.UTF-8/man1/wine.1
mkdir -p %{buildroot}%{_mandir}/pl.UTF-8/man1
install -p -m 0644 loader/wine.pl.UTF-8.man %{buildroot}%{_mandir}/pl.UTF-8/man1/wine.1


%if 0%{?rhel} == 6
%post sysvinit
if [ $1 -eq 1 ]; then
/sbin/chkconfig --add wine
/sbin/chkconfig --level 2345 wine on
/sbin/service wine start &>/dev/null || :
fi

%preun sysvinit
if [ $1 -eq 0 ]; then
/sbin/service wine stop >/dev/null 2>&1
/sbin/chkconfig --del wine
fi
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} > 6
%post systemd
%binfmt_apply wine.conf

%postun systemd
if [ $1 -eq 0 ]; then
/bin/systemctl try-restart systemd-binfmt.service
fi
%endif

%ldconfig_post core

%posttrans core
%ifarch x86_64 aarch64
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine64 10 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine64-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver64 20
%else
%ifnarch %{arm}
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20 \
  --slave %{_bindir}/wine-preloader wine-preloader %{_bindir}/wine32-preloader
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%else
%{_sbindir}/alternatives --install %{_bindir}/wine \
  wine %{_bindir}/wine32 20
%{_sbindir}/alternatives --install %{_bindir}/wineserver \
  wineserver %{_bindir}/wineserver32 10
%endif
%endif
%{_sbindir}/alternatives --install %{_libdir}/wine/dxgi.dll.so \
  wine-dxgi %{_libdir}/wine/wine-dxgi.dll.so 10
%{_sbindir}/alternatives --install %{_libdir}/wine/d3d9.%{winedll} \
  wine-d3d9 %{_libdir}/wine/wine-d3d9.%{winedll} 10
%{_sbindir}/alternatives --install %{_libdir}/wine/d3d10.%{winedll} \
  wine-d3d10 %{_libdir}/wine/wine-d3d10.%{winedll} 10 \
  --slave  %{_libdir}/wine/d3d10_1.%{winedll} wine-d3d10_1 %{_libdir}/wine/wine-d3d10_1.%{winedll} \
  --slave  %{_libdir}/wine/d3d10core.%{winedll} wine-d3d10core %{_libdir}/wine/wine-d3d10core.%{winedll}
%{_sbindir}/alternatives --install %{_libdir}/wine/d3d11.%{winedll} \
  wine-d3d11 %{_libdir}/wine/wine-d3d11.%{winedll} 10

%postun core
%{?ldconfig}
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
  %{_sbindir}/alternatives --remove wine-dxgi %{_libdir}/wine/wine-dxgi.dll.so
  %{_sbindir}/alternatives --remove wine-d3d9 %{_libdir}/wine/wine-d3d9.%{winedll}
  %{_sbindir}/alternatives --remove wine-d3d10 %{_libdir}/wine/wine-d3d10.%{winedll}
  %{_sbindir}/alternatives --remove wine-d3d11 %{_libdir}/wine/wine-d3d11.%{winedll}
fi

%ldconfig_scriptlets ldap

%ldconfig_scriptlets cms

%ldconfig_scriptlets twain

%ldconfig_scriptlets capi

%ldconfig_scriptlets alsa

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%ldconfig_scriptlets openal
%endif

%files
# meta package

%files core
%doc ANNOUNCE
%doc COPYING.LIB
%doc LICENSE
%doc LICENSE.OLD
%doc AUTHORS
%doc README-FEDORA
%doc README
%doc VERSION
# do not include huge changelogs .OLD .ALPHA .BETA (#204302)
%doc documentation/README.*
%if 0%{?wine_staging}
%{_bindir}/msidb
%{_libdir}/wine/runas.exe.so
%endif
%{_bindir}/winedump
%{_libdir}/wine/explorer.%{wineexe}
%{_libdir}/wine/cabarc.%{wineexe}
%{_libdir}/wine/control.%{wineexe}
%{_libdir}/wine/cmd.%{wineexe}
%{_libdir}/wine/dxdiag.%{wineexe}
%{_libdir}/wine/notepad.%{wineexe}
%{_libdir}/wine/plugplay.%{wineexe}
%{_libdir}/wine/progman.%{wineexe}
%{_libdir}/wine/taskmgr.%{wineexe}
%{_libdir}/wine/winedbg.exe.so
%{_libdir}/wine/winefile.%{wineexe}
%{_libdir}/wine/winemine.%{wineexe}
%{_libdir}/wine/winemsibuilder.%{wineexe}
%{_libdir}/wine/winepath.exe.so
%{_libdir}/wine/winmgmt.%{wineexe}
%{_libdir}/wine/winver.exe.so
%{_libdir}/wine/wordpad.%{wineexe}
%{_libdir}/wine/write.%{wineexe}
%{_libdir}/wine/wusa.exe.so

%ifarch %{ix86} %{arm}
%{_bindir}/wine32
%ifnarch %{arm}
%{_bindir}/wine32-preloader
%endif
%{_bindir}/wineserver32
%config %{_sysconfdir}/ld.so.conf.d/wine-32.conf
%endif

%ifarch x86_64 aarch64
%{_bindir}/wine64
%{_bindir}/wineserver64
%config %{_sysconfdir}/ld.so.conf.d/wine-64.conf
%endif
%ifarch x86_64 aarch64
%{_bindir}/wine64-preloader
%endif

%ghost %{_bindir}/wine
%ifnarch %{arm}
%ghost %{_bindir}/wine-preloader
%endif
%ghost %{_bindir}/wineserver

%dir %{_libdir}/wine
%dir %{_libdir}/wine/fakedlls
%{_libdir}/wine/fakedlls/*

%{_libdir}/wine/attrib.%{wineexe}
%{_libdir}/wine/arp.%{wineexe}
%{_libdir}/wine/aspnet_regiis.%{wineexe}
%{_libdir}/wine/cacls.%{wineexe}
%{_libdir}/wine/conhost.%{wineexe}
%{_libdir}/wine/cscript.%{wineexe}
%{_libdir}/wine/dism.%{wineexe}
%{_libdir}/wine/dpnsvr.%{wineexe}
%{_libdir}/wine/eject.%{wineexe}
%{_libdir}/wine/expand.%{wineexe}
%{_libdir}/wine/extrac32.%{wineexe}
%{_libdir}/wine/fc.%{wineexe}
%{_libdir}/wine/find.%{wineexe}
%{_libdir}/wine/findstr.%{wineexe}
%{_libdir}/wine/fsutil.exe.so
%{_libdir}/wine/hostname.%{wineexe}
%{_libdir}/wine/ipconfig.%{wineexe}
%{_libdir}/wine/winhlp32.%{wineexe}
%{_libdir}/wine/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/msidb.%{wineexe}
%endif
%{_libdir}/wine/msiexec.%{wineexe}
%{_libdir}/wine/net.%{wineexe}
%{_libdir}/wine/netstat.%{wineexe}
%{_libdir}/wine/ngen.%{wineexe}
%{_libdir}/wine/ntoskrnl.%{wineexe}
%{_libdir}/wine/oleview.%{wineexe}
%{_libdir}/wine/ping.%{wineexe}
%{_libdir}/wine/powershell.%{wineexe}
%{_libdir}/wine/reg.%{wineexe}
%{_libdir}/wine/regasm.%{wineexe}
%{_libdir}/wine/regedit.%{wineexe}
%{_libdir}/wine/regsvcs.%{wineexe}
%{_libdir}/wine/regsvr32.%{wineexe}
%{_libdir}/wine/rpcss.%{wineexe}
%{_libdir}/wine/rundll32.%{wineexe}
%{_libdir}/wine/schtasks.%{wineexe}
%{_libdir}/wine/sdbinst.%{wineexe}
%{_libdir}/wine/secedit.%{wineexe}
%{_libdir}/wine/servicemodelreg.%{wineexe}
%{_libdir}/wine/services.%{wineexe}
%{_libdir}/wine/start.%{wineexe}
%{_libdir}/wine/tasklist.%{wineexe}
%{_libdir}/wine/termsv.%{wineexe}
%{_libdir}/wine/view.%{wineexe}
%{_libdir}/wine/wevtutil.%{wineexe}
%{_libdir}/wine/wineboot.%{wineexe}
%{_libdir}/wine/winebrowser.exe.so
%{_libdir}/wine/wineconsole.exe.so
%{_libdir}/wine/winemenubuilder.exe.so
%{_libdir}/wine/winecfg.exe.so
%{_libdir}/wine/winedevice.%{wineexe}
%{_libdir}/wine/wmplayer.%{wineexe}
%{_libdir}/wine/wscript.%{wineexe}
%{_libdir}/wine/uninstaller.%{wineexe}

%{_libdir}/libwine.so.1*

%{_libdir}/wine/acledit.%{winedll}
%{_libdir}/wine/aclui.%{winedll}
%{_libdir}/wine/activeds.%{winedll}
%{_libdir}/wine/actxprxy.%{winedll}
%{_libdir}/wine/adsldp.%{winedll}
%{_libdir}/wine/adsldpc.%{winedll}
%{_libdir}/wine/advapi32.dll.so
%{_libdir}/wine/advpack.%{winedll}
%{_libdir}/wine/amsi.%{winedll}
%{_libdir}/wine/amstream.dll.so
%{_libdir}/wine/api-ms-win-appmodel-identity-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-appmodel-runtime-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-apiquery-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-appcompat-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-appinit-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-atoms-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-bem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-com-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-comm-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-console-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-crt-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-datetime-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-debug-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-delayload-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-errorhandling-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-fibers-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-file-l2-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-handle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-heap-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-interlocked-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-io-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-job-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-largeinteger-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-legacy-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-kernel32-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-libraryloader-l1-2-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-obsolete-l1-3-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localization-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-localregistry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-memory-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-misc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namedpipe-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-namespace-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-normalization-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-path-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-privateprofile-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processenvironment-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-2.%{winedll}
%{_libdir}/wine/api-ms-win-core-processthreads-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-core-processtopology-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-profile-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-psapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-quirks-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-realtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registry-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-registryuserspecific-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-rtlsupport-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shlwapi-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-shutdown-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sidebyside-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-string-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-stringloader-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-synch-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-sysinfo-l1-2-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-threadpool-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-timezone-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-toolhelp-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-url-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-util-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-version-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-versionansi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-windowserrorreporting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-error-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-errorprivate-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-registration-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-roparameterizediid-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-winrt-string-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-wow64-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-core-xstate-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-conio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-convert-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-environment-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-filesystem-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-heap-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-locale-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-math-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-multibyte-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-process-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-runtime-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-stdio-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-string-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-crt-utility-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-devices-config-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-devices-query-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-advapi32-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-normaliz-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-ole32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shell32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-shlwapi-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-user32-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-downlevel-version-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-dx-d3dkmt-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-classicprovider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-consumer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-controller-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventing-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-eventlog-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-gdi-dpiinfo-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-joystick-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-misc-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-mm-mme-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-mm-time-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-rectangle-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-perf-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-power-setting-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-private-l1-1-4.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-winevent-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.%{winedll}
%{_libdir}/wine/api-ms-win-security-activedirectoryclient-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-audit-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-base-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-credentials-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-cryptoapi-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-grouppolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsalookup-l2-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-security-lsapolicy-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-provider-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-sddl-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-security-systemfunctions-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-core-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-management-l2-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-private-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-service-winsvc-l1-2-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-scaling-l1-1-1.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-stream-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shcore-thread-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellcom-l1-1-0.%{winedll}
%{_libdir}/wine/api-ms-win-shell-shellfolders-l1-1-0.%{winedll}
%{_libdir}/wine/apphelp.%{winedll}
%{_libdir}/wine/appwiz.%{winecpl}
%{_libdir}/wine/atl.%{winedll}
%{_libdir}/wine/atl80.%{winedll}
%{_libdir}/wine/atl90.%{winedll}
%{_libdir}/wine/atl100.%{winedll}
%{_libdir}/wine/atl110.%{winedll}
%{_libdir}/wine/atlthunk.%{winedll}
%{_libdir}/wine/atmlib.%{winedll}
%{_libdir}/wine/authz.%{winedll}
%{_libdir}/wine/avicap32.dll.so
%{_libdir}/wine/avifil32.%{winedll}
%{_libdir}/wine/avrt.%{winedll}
%{_libdir}/wine/bcrypt.dll.so
%{_libdir}/wine/bluetoothapis.%{winedll}
%{_libdir}/wine/browseui.%{winedll}
%{_libdir}/wine/bthprops.%{winecpl}
%{_libdir}/wine/cabinet.dll.so
%{_libdir}/wine/cards.%{winedll}
%{_libdir}/wine/cdosys.%{winedll}
%{_libdir}/wine/cfgmgr32.%{winedll}
%{_libdir}/wine/clock.%{wineexe}
%{_libdir}/wine/clusapi.%{winedll}
%{_libdir}/wine/combase.%{winedll}
%{_libdir}/wine/comcat.%{winedll}
%{_libdir}/wine/comctl32.%{winedll}
%{_libdir}/wine/comdlg32.%{winedll}
%{_libdir}/wine/compstui.%{winedll}
%{_libdir}/wine/comsvcs.%{winedll}
%{_libdir}/wine/concrt140.%{winedll}
%{_libdir}/wine/connect.%{winedll}
%{_libdir}/wine/credui.%{winedll}
%{_libdir}/wine/crtdll.dll.so
%{_libdir}/wine/crypt32.dll.so
%{_libdir}/wine/cryptdlg.%{winedll}
%{_libdir}/wine/cryptdll.%{winedll}
%{_libdir}/wine/cryptext.%{winedll}
%{_libdir}/wine/cryptnet.%{winedll}
%{_libdir}/wine/cryptui.%{winedll}
%{_libdir}/wine/ctapi32.dll.so
%{_libdir}/wine/ctl3d32.%{winedll}
%{_libdir}/wine/d2d1.%{winedll}
%ghost %{_libdir}/wine/d3d10.%{winedll}
%ghost %{_libdir}/wine/d3d10_1.%{winedll}
%ghost %{_libdir}/wine/d3d10core.%{winedll}
%{_libdir}/wine/wine-d3d10.%{winedll}
%{_libdir}/wine/wine-d3d10_1.%{winedll}
%{_libdir}/wine/wine-d3d10core.%{winedll}
%ghost %{_libdir}/wine/d3d11.%{winedll}
%{_libdir}/wine/wine-d3d11.%{winedll}
%{_libdir}/wine/d3d12.dll.so
%{_libdir}/wine/d3dcompiler_*.%{winedll}
%{_libdir}/wine/d3dim.%{winedll}
%{_libdir}/wine/d3drm.%{winedll}
%{_libdir}/wine/d3dx9_*.%{winedll}
%{_libdir}/wine/d3dx10_*.%{winedll}
%{_libdir}/wine/d3dx11_42.%{winedll}
%{_libdir}/wine/d3dx11_43.%{winedll}
%{_libdir}/wine/d3dxof.%{winedll}
%{_libdir}/wine/davclnt.%{winedll}
%{_libdir}/wine/dbgeng.%{winedll}
%{_libdir}/wine/dbghelp.dll.so
%{_libdir}/wine/dciman32.%{winedll}
%{_libdir}/wine/ddraw.%{winedll}
%{_libdir}/wine/ddrawex.%{winedll}
%{_libdir}/wine/devenum.%{winedll}
%{_libdir}/wine/dhcpcsvc.%{winedll}
%{_libdir}/wine/dhtmled.%{wineocx}
%{_libdir}/wine/difxapi.%{winedll}
%{_libdir}/wine/dinput.dll.so
%{_libdir}/wine/dinput8.dll.so
%{_libdir}/wine/directmanipulation.%{winedll}
%{_libdir}/wine/dispex.%{winedll}
%{_libdir}/wine/dmband.%{winedll}
%{_libdir}/wine/dmcompos.%{winedll}
%{_libdir}/wine/dmime.%{winedll}
%{_libdir}/wine/dmloader.%{winedll}
%{_libdir}/wine/dmscript.%{winedll}
%{_libdir}/wine/dmstyle.%{winedll}
%{_libdir}/wine/dmsynth.%{winedll}
%{_libdir}/wine/dmusic.%{winedll}
%{_libdir}/wine/dmusic32.%{winedll}
%{_libdir}/wine/dplay.%{winedll}
%{_libdir}/wine/dplayx.%{winedll}
%{_libdir}/wine/dpnaddr.%{winedll}
%{_libdir}/wine/dpnet.%{winedll}
%{_libdir}/wine/dpnhpast.%{winedll}
%{_libdir}/wine/dpnlobby.%{winedll}
%{_libdir}/wine/dpvoice.%{winedll}
%{_libdir}/wine/dpwsockx.%{winedll}
%{_libdir}/wine/drmclien.%{winedll}
%{_libdir}/wine/dsound.%{winedll}
%{_libdir}/wine/dsquery.%{winedll}
%{_libdir}/wine/dssenh.%{winedll}
%{_libdir}/wine/dswave.%{winedll}
%{_libdir}/wine/dwmapi.%{winedll}
%{_libdir}/wine/dwrite.dll.so
%{_libdir}/wine/dx8vb.%{winedll}
%{_libdir}/wine/dxdiagn.%{winedll}
%ghost %{_libdir}/wine/dxgi.dll.so
%{_libdir}/wine/wine-dxgi.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/dxgkrnl.%{winesys}
%{_libdir}/wine/dxgmms1.%{winesys}
%endif
%{_libdir}/wine/dxva2.dll.so
%{_libdir}/wine/esent.%{winedll}
%{_libdir}/wine/evr.%{winedll}
%{_libdir}/wine/explorerframe.%{winedll}
%{_libdir}/wine/ext-ms-win-authz-context-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-domainjoin-netjoin-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-dwmapi-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-dc-create-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-draw-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-font-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-gdi-render-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-kernel32-package-current-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-dialogbox-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-gui-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-keyboard-l1-3-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-5-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-message-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-misc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-mouse-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-private-l1-3-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-rectangle-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-uicontext-ext-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-window-l1-1-4.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ntuser-windowclass-l1-1-1.%{winedll}
%{_libdir}/wine/ext-ms-win-oleacc-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-ras-rasapi32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-object-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-gdi-rgn-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-credui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-security-cryptui-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comctl32-init-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-comdlg32-l1-1-0.%{winedll}
%{_libdir}/wine/ext-ms-win-shell-shell32-l1-2-0.%{winedll}
%{_libdir}/wine/ext-ms-win-uxtheme-themes-l1-1-0.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/faultrep.%{winedll}
%{_libdir}/wine/feclient.%{winedll}
%{_libdir}/wine/fltlib.%{winedll}
%{_libdir}/wine/fltmgr.%{winesys}
%{_libdir}/wine/fntcache.%{winedll}
%{_libdir}/wine/fontsub.%{winedll}
%{_libdir}/wine/fusion.%{winedll}
%{_libdir}/wine/fwpuclnt.%{winedll}
%{_libdir}/wine/gameux.%{winedll}
%{_libdir}/wine/gdi32.dll.so
%{_libdir}/wine/gdiplus.%{winedll}
%{_libdir}/wine/glu32.dll.so
%{_libdir}/wine/gphoto2.ds.so
%{_libdir}/wine/gpkcsp.%{winedll}
%{_libdir}/wine/hal.%{winedll}
%{_libdir}/wine/hh.%{wineexe}
%{_libdir}/wine/hhctrl.%{wineocx}
%{_libdir}/wine/hid.%{winedll}
%{_libdir}/wine/hidclass.%{winesys}
%{_libdir}/wine/hlink.%{winedll}
%{_libdir}/wine/hnetcfg.%{winedll}
%{_libdir}/wine/httpapi.%{winedll}
%{_libdir}/wine/icacls.%{wineexe}
%{_libdir}/wine/iccvid.%{winedll}
%{_libdir}/wine/icinfo.%{wineexe}
%{_libdir}/wine/icmp.%{winedll}
%{_libdir}/wine/ieframe.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/iertutil.dll.so
%endif
%{_libdir}/wine/ieproxy.%{winedll}
%{_libdir}/wine/imaadp32.%{wineacm}
%{_libdir}/wine/imagehlp.%{winedll}
%{_libdir}/wine/imm32.%{winedll}
%{_libdir}/wine/inetcomm.%{winedll}
%{_libdir}/wine/inetcpl.%{winecpl}
%{_libdir}/wine/inetmib1.%{winedll}
%{_libdir}/wine/infosoft.%{winedll}
%{_libdir}/wine/initpki.%{winedll}
%{_libdir}/wine/inkobj.%{winedll}
%{_libdir}/wine/inseng.%{winedll}
%{_libdir}/wine/iphlpapi.dll.so
%{_libdir}/wine/iprop.%{winedll}
%{_libdir}/wine/irprops.%{winecpl}
%{_libdir}/wine/itircl.%{winedll}
%{_libdir}/wine/itss.%{winedll}
%{_libdir}/wine/joy.%{winecpl}
%{_libdir}/wine/jscript.%{winedll}
%{_libdir}/wine/jsproxy.%{winedll}
%{_libdir}/wine/kerberos.dll.so
%{_libdir}/wine/kernel32.dll.so
%{_libdir}/wine/kernelbase.%{winedll}
%{_libdir}/wine/ksecdd.%{winesys}
%{_libdir}/wine/ksuser.%{winedll}
%{_libdir}/wine/ktmw32.%{winedll}
%if 0%{?fedora} > 24
%{_libdir}/wine/l3codeca.acm.so
%endif
%{_libdir}/wine/loadperf.%{winedll}
%{_libdir}/wine/localspl.%{winedll}
%{_libdir}/wine/localui.%{winedll}
%{_libdir}/wine/lodctr.%{wineexe}
%{_libdir}/wine/lz32.%{winedll}
%{_libdir}/wine/mapi32.%{winedll}
%{_libdir}/wine/mapistub.%{winedll}
%{_libdir}/wine/mciavi32.%{winedll}
%{_libdir}/wine/mcicda.%{winedll}
%{_libdir}/wine/mciqtz32.%{winedll}
%{_libdir}/wine/mciseq.%{winedll}
%{_libdir}/wine/mciwave.%{winedll}
%{_libdir}/wine/mf.%{winedll}
%{_libdir}/wine/mf3216.%{winedll}
%{_libdir}/wine/mferror.%{winedll}
%{_libdir}/wine/mfplat.%{winedll}
%{_libdir}/wine/mfplay.%{winedll}
%{_libdir}/wine/mfreadwrite.%{winedll}
%{_libdir}/wine/mgmtapi.%{winedll}
%{_libdir}/wine/midimap.%{winedll}
%{_libdir}/wine/mlang.%{winedll}
%{_libdir}/wine/mmcndmgr.%{winedll}
%{_libdir}/wine/mmdevapi.%{winedll}
%{_libdir}/wine/mofcomp.%{wineexe}
%{_libdir}/wine/mountmgr.sys.so
%{_libdir}/wine/mp3dmod.dll.so
%{_libdir}/wine/mpr.%{winedll}
%{_libdir}/wine/mprapi.%{winedll}
%{_libdir}/wine/msacm32.%{winedll}
%{_libdir}/wine/msacm32.%{winedrv}
%{_libdir}/wine/msadp32.%{wineacm}
%{_libdir}/wine/msasn1.%{winedll}
%{_libdir}/wine/mscat32.%{winedll}
%{_libdir}/wine/mscoree.%{winedll}
%{_libdir}/wine/mscorwks.%{winedll}
%{_libdir}/wine/msctf.%{winedll}
%{_libdir}/wine/msctfp.%{winedll}
%{_libdir}/wine/msdaps.%{winedll}
%{_libdir}/wine/msdelta.%{winedll}
%{_libdir}/wine/msdmo.%{winedll}
%{_libdir}/wine/msdrm.%{winedll}
%{_libdir}/wine/msftedit.%{winedll}
%{_libdir}/wine/msg711.%{wineacm}
%{_libdir}/wine/msgsm32.acm.so
%{_libdir}/wine/mshtml.%{winedll}
%{_libdir}/wine/mshtml.%{winetlb}
%{_libdir}/wine/msi.%{winedll}
%{_libdir}/wine/msident.%{winedll}
%{_libdir}/wine/msimtf.%{winedll}
%{_libdir}/wine/msimg32.%{winedll}
%{_libdir}/wine/msimsg.%{winedll}
%{_libdir}/wine/msinfo32.%{wineexe}
%{_libdir}/wine/msisip.%{winedll}
%{_libdir}/wine/msisys.%{wineocx}
%{_libdir}/wine/msls31.%{winedll}
%{_libdir}/wine/msnet32.%{winedll}
%{_libdir}/wine/mspatcha.%{winedll}
%{_libdir}/wine/msports.%{winedll}
%{_libdir}/wine/msscript.%{wineocx}
%{_libdir}/wine/mssign32.%{winedll}
%{_libdir}/wine/mssip32.%{winedll}
%{_libdir}/wine/msrle32.%{winedll}
%{_libdir}/wine/mstask.%{winedll}
%{_libdir}/wine/msvcirt.%{winedll}
%{_libdir}/wine/msvcm80.%{winedll}
%{_libdir}/wine/msvcm90.%{winedll}
%{_libdir}/wine/msvcp60.%{winedll}
%{_libdir}/wine/msvcp70.%{winedll}
%{_libdir}/wine/msvcp71.%{winedll}
%{_libdir}/wine/msvcp80.%{winedll}
%{_libdir}/wine/msvcp90.%{winedll}
%{_libdir}/wine/msvcp100.%{winedll}
%{_libdir}/wine/msvcp110.%{winedll}
%{_libdir}/wine/msvcp120.%{winedll}
%{_libdir}/wine/msvcp120_app.%{winedll}
%{_libdir}/wine/msvcp140.%{winedll}
%{_libdir}/wine/msvcr70.dll.so
%{_libdir}/wine/msvcr71.dll.so
%{_libdir}/wine/msvcr80.dll.so
%{_libdir}/wine/msvcr90.dll.so
%{_libdir}/wine/msvcr100.dll.so
%{_libdir}/wine/msvcr110.dll.so
%{_libdir}/wine/msvcr120.dll.so
%{_libdir}/wine/msvcr120_app.%{winedll}
%{_libdir}/wine/msvcrt.dll.so
%{_libdir}/wine/msvcrt20.%{winedll}
%{_libdir}/wine/msvcrt40.%{winedll}
%{_libdir}/wine/msvcrtd.dll.so
%{_libdir}/wine/msvfw32.%{winedll}
%{_libdir}/wine/msvidc32.%{winedll}
%{_libdir}/wine/mswsock.%{winedll}
%{_libdir}/wine/msxml.%{winedll}
%{_libdir}/wine/msxml2.%{winedll}
%{_libdir}/wine/msxml3.dll.so
%{_libdir}/wine/msxml4.%{winedll}
%{_libdir}/wine/msxml6.%{winedll}
%{_libdir}/wine/mtxdm.%{winedll}
%{_libdir}/wine/nddeapi.%{winedll}
%{_libdir}/wine/ncrypt.%{winedll}
%{_libdir}/wine/ndis.%{winesys}
%{_libdir}/wine/netapi32.dll.so
%{_libdir}/wine/netcfgx.%{winedll}
%{_libdir}/wine/netprofm.%{winedll}
%{_libdir}/wine/netsh.%{wineexe}
%{_libdir}/wine/newdev.%{winedll}
%{_libdir}/wine/ninput.%{winedll}
%{_libdir}/wine/normaliz.%{winedll}
%{_libdir}/wine/npmshtml.%{winedll}
%{_libdir}/wine/npptools.%{winedll}
%{_libdir}/wine/ntdll.dll.so
%{_libdir}/wine/ntdsapi.%{winedll}
%{_libdir}/wine/ntprint.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/nvcuda.dll.so
%{_libdir}/wine/nvcuvid.dll.so
%endif
%{_libdir}/wine/objsel.%{winedll}
%{_libdir}/wine/odbc32.dll.so
%{_libdir}/wine/odbccp32.%{winedll}
%{_libdir}/wine/odbccu32.%{winedll}
%{_libdir}/wine/ole32.%{winedll}
%{_libdir}/wine/oleacc.%{winedll}
%{_libdir}/wine/oleaut32.%{winedll}
%{_libdir}/wine/olecli32.%{winedll}
%{_libdir}/wine/oledb32.%{winedll}
%{_libdir}/wine/oledlg.%{winedll}
%{_libdir}/wine/olepro32.%{winedll}
%{_libdir}/wine/olesvr32.%{winedll}
%{_libdir}/wine/olethk32.%{winedll}
%{_libdir}/wine/opcservices.dll.so
%{_libdir}/wine/packager.%{winedll}
%{_libdir}/wine/pdh.%{winedll}
%{_libdir}/wine/photometadatahandler.%{winedll}
%{_libdir}/wine/pidgen.%{winedll}
%{_libdir}/wine/powrprof.%{winedll}
%{_libdir}/wine/presentationfontcache.%{wineexe}
%{_libdir}/wine/printui.%{winedll}
%{_libdir}/wine/prntvpt.%{winedll}
%{_libdir}/wine/propsys.%{winedll}
%{_libdir}/wine/psapi.%{winedll}
%{_libdir}/wine/pstorec.%{winedll}
%{_libdir}/wine/qcap.dll.so
%{_libdir}/wine/qedit.%{winedll}
%{_libdir}/wine/qmgr.%{winedll}
%{_libdir}/wine/qmgrprxy.%{winedll}
%{_libdir}/wine/quartz.dll.so
%{_libdir}/wine/query.%{winedll}
%{_libdir}/wine/qwave.%{winedll}
%{_libdir}/wine/rasapi32.%{winedll}
%{_libdir}/wine/rasdlg.%{winedll}
%{_libdir}/wine/regapi.%{winedll}
%{_libdir}/wine/resutils.%{winedll}
%{_libdir}/wine/riched20.%{winedll}
%{_libdir}/wine/riched32.%{winedll}
%{_libdir}/wine/rpcrt4.%{winedll}
%{_libdir}/wine/rsabase.%{winedll}
%{_libdir}/wine/rsaenh.%{winedll}
%{_libdir}/wine/rstrtmgr.%{winedll}
%{_libdir}/wine/rtutils.%{winedll}
%{_libdir}/wine/samlib.%{winedll}
%{_libdir}/wine/sapi.%{winedll}
%{_libdir}/wine/sas.%{winedll}
%{_libdir}/wine/sc.%{wineexe}
%{_libdir}/wine/scarddlg.%{winedll}
%{_libdir}/wine/sccbase.%{winedll}
%{_libdir}/wine/schannel.%{winedll}
%{_libdir}/wine/scrobj.%{winedll}
%{_libdir}/wine/scrrun.%{winedll}
%{_libdir}/wine/scsiport.%{winesys}
%{_libdir}/wine/secur32.dll.so
%{_libdir}/wine/sensapi.%{winedll}
%{_libdir}/wine/serialui.%{winedll}
%{_libdir}/wine/setupapi.%{winedll}
%{_libdir}/wine/sfc_os.%{winedll}
%{_libdir}/wine/shcore.%{winedll}
%{_libdir}/wine/shdoclc.%{winedll}
%{_libdir}/wine/shdocvw.%{winedll}
%{_libdir}/wine/schedsvc.%{winedll}
%{_libdir}/wine/shell32.dll.so
%{_libdir}/wine/shfolder.%{winedll}
%{_libdir}/wine/shlwapi.%{winedll}
%{_libdir}/wine/shutdown.%{wineexe}
%{_libdir}/wine/slbcsp.%{winedll}
%{_libdir}/wine/slc.%{winedll}
%{_libdir}/wine/snmpapi.%{winedll}
%{_libdir}/wine/softpub.%{winedll}
%{_libdir}/wine/spoolsv.%{wineexe}
%{_libdir}/wine/srclient.%{winedll}
%{_libdir}/wine/sspicli.%{winedll}
%{_libdir}/wine/stdole2.%{winetlb}
%{_libdir}/wine/stdole32.%{winetlb}
%{_libdir}/wine/sti.%{winedll}
%{_libdir}/wine/strmdll.%{winedll}
%{_libdir}/wine/subst.%{wineexe}
%{_libdir}/wine/svchost.%{wineexe}
%{_libdir}/wine/svrapi.%{winedll}
%{_libdir}/wine/sxs.%{winedll}
%{_libdir}/wine/systeminfo.%{wineexe}
%{_libdir}/wine/t2embed.%{winedll}
%{_libdir}/wine/tapi32.%{winedll}
%{_libdir}/wine/taskkill.%{wineexe}
%{_libdir}/wine/taskschd.%{winedll}
%{_libdir}/wine/tdh.%{winedll}
%{_libdir}/wine/tdi.%{winesys}
%{_libdir}/wine/traffic.%{winedll}
%{_libdir}/wine/tzres.%{winedll}
%{_libdir}/wine/ucrtbase.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/uianimation.%{winedll}
%endif
%{_libdir}/wine/uiautomationcore.%{winedll}
%{_libdir}/wine/uiribbon.%{winedll}
%{_libdir}/wine/unicows.%{winedll}
%{_libdir}/wine/unlodctr.%{wineexe}
%{_libdir}/wine/updspapi.%{winedll}
%{_libdir}/wine/url.%{winedll}
%{_libdir}/wine/urlmon.%{winedll}
%{_libdir}/wine/usbd.%{winesys}
%{_libdir}/wine/user32.dll.so
%{_libdir}/wine/usp10.%{winedll}
%{_libdir}/wine/uxtheme.dll.so
%{_libdir}/wine/userenv.%{winedll}
%{_libdir}/wine/vbscript.%{winedll}
%{_libdir}/wine/vcomp.%{winedll}
%{_libdir}/wine/vcomp90.%{winedll}
%{_libdir}/wine/vcomp100.%{winedll}
%{_libdir}/wine/vcomp110.%{winedll}
%{_libdir}/wine/vcomp120.%{winedll}
%{_libdir}/wine/vcomp140.%{winedll}
%{_libdir}/wine/vcruntime140.%{winedll}
%{_libdir}/wine/vdmdbg.%{winedll}
%{_libdir}/wine/version.%{winedll}
%{_libdir}/wine/virtdisk.%{winedll}
%{_libdir}/wine/vssapi.%{winedll}
%{_libdir}/wine/vulkan-1.%{winedll}
%{_libdir}/wine/wbemdisp.%{winedll}
%{_libdir}/wine/wbemprox.%{winedll}
%{_libdir}/wine/wdscore.%{winedll}
%{_libdir}/wine/webservices.%{winedll}
%{_libdir}/wine/wer.%{winedll}
%{_libdir}/wine/wevtapi.%{winedll}
%{_libdir}/wine/wiaservc.%{winedll}
%{_libdir}/wine/wimgapi.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/win32k.%{winesys}
%endif
%{_libdir}/wine/windowscodecs.dll.so
%{_libdir}/wine/windowscodecsext.%{winedll}
%{_libdir}/wine/winebus.sys.so
%{_libdir}/wine/winegstreamer.dll.so
%{_libdir}/wine/winehid.%{winesys}
%{_libdir}/wine/winejoystick.drv.so
%{_libdir}/wine/winemapi.%{winedll}
%{_libdir}/wine/winevulkan.dll.so
%{_libdir}/wine/winex11.drv.so
%{_libdir}/wine/wing32.%{winedll}
%{_libdir}/wine/winhttp.dll.so
%{_libdir}/wine/wininet.dll.so
%{_libdir}/wine/winmm.%{winedll}
%{_libdir}/wine/winnls32.%{winedll}
%{_libdir}/wine/winspool.drv.so
%{_libdir}/wine/winsta.%{winedll}
%{_libdir}/wine/wmasf.%{winedll}
%{_libdir}/wine/wmi.%{winedll}
%{_libdir}/wine/wmic.%{wineexe}
%{_libdir}/wine/wmiutils.%{winedll}
%{_libdir}/wine/wmp.%{winedll}
%{_libdir}/wine/wmvcore.%{winedll}
%{_libdir}/wine/spoolss.%{winedll}
%{_libdir}/wine/winscard.%{winedll}
%{_libdir}/wine/wintab32.%{winedll}
%{_libdir}/wine/wintrust.%{winedll}
%{_libdir}/wine/winusb.%{winedll}
%{_libdir}/wine/wlanapi.%{winedll}
%{_libdir}/wine/wmphoto.%{winedll}
%{_libdir}/wine/wnaspi32.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/wow64cpu.dll.so
%endif
%{_libdir}/wine/wpc.%{winedll}
%{_libdir}/wine/wpcap.dll.so
%{_libdir}/wine/ws2_32.dll.so
%{_libdir}/wine/wsdapi.%{winedll}
%{_libdir}/wine/wshom.%{wineocx}
%{_libdir}/wine/wsnmp32.%{winedll}
%{_libdir}/wine/wsock32.%{winedll}
%{_libdir}/wine/wtsapi32.%{winedll}
%{_libdir}/wine/wuapi.%{winedll}
%{_libdir}/wine/wuaueng.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/wuauserv.%{wineexe}
%endif
%{_libdir}/wine/security.%{winedll}
%{_libdir}/wine/sfc.%{winedll}
%{_libdir}/wine/wineps.%{winedrv}
%{_libdir}/wine/d3d8.%{winedll}
%ghost %{_libdir}/wine/d3d9.%{winedll}
%{_libdir}/wine/wine-d3d9.%{winedll}
%{_libdir}/wine/opengl32.dll.so
%{_libdir}/wine/wined3d.dll.so
%{_libdir}/wine/dnsapi.dll.so
%{_libdir}/wine/iexplore.%{wineexe}
%{_libdir}/wine/x3daudio1_0.dll.so
%{_libdir}/wine/x3daudio1_1.dll.so
%{_libdir}/wine/x3daudio1_2.dll.so
%{_libdir}/wine/x3daudio1_3.dll.so
%{_libdir}/wine/x3daudio1_4.dll.so
%{_libdir}/wine/x3daudio1_5.dll.so
%{_libdir}/wine/x3daudio1_6.dll.so
%{_libdir}/wine/x3daudio1_7.dll.so
%{_libdir}/wine/xapofx1_1.dll.so
%{_libdir}/wine/xapofx1_2.dll.so
%{_libdir}/wine/xapofx1_3.dll.so
%{_libdir}/wine/xapofx1_4.dll.so
%{_libdir}/wine/xapofx1_5.dll.so
%{_libdir}/wine/xaudio2_0.dll.so
%{_libdir}/wine/xaudio2_1.dll.so
%{_libdir}/wine/xaudio2_2.dll.so
%{_libdir}/wine/xaudio2_3.dll.so
%{_libdir}/wine/xaudio2_4.dll.so
%{_libdir}/wine/xaudio2_5.dll.so
%{_libdir}/wine/xaudio2_6.dll.so
%{_libdir}/wine/xaudio2_7.dll.so
%{_libdir}/wine/xaudio2_8.dll.so
%{_libdir}/wine/xaudio2_9.dll.so
%{_libdir}/wine/xcopy.%{wineexe}
%{_libdir}/wine/xinput1_1.%{winedll}
%{_libdir}/wine/xinput1_2.%{winedll}
%{_libdir}/wine/xinput1_3.%{winedll}
%{_libdir}/wine/xinput1_4.%{winedll}
%{_libdir}/wine/xinput9_1_0.%{winedll}
%{_libdir}/wine/xmllite.%{winedll}
%{_libdir}/wine/xolehlp.%{winedll}
%{_libdir}/wine/xpsprint.%{winedll}
%{_libdir}/wine/xpssvcs.%{winedll}

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/nvapi64.dll.so
%{_libdir}/wine/nvencodeapi64.dll.so
%else
%{_libdir}/wine/nvapi.dll.so
%{_libdir}/wine/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/winevdm.exe.so
%{_libdir}/wine/ifsmgr.vxd
%{_libdir}/wine/mmdevldr.vxd
%{_libdir}/wine/monodebg.vxd
%{_libdir}/wine/rundll.exe16
%{_libdir}/wine/vdhcp.vxd
%{_libdir}/wine/user.exe16
%{_libdir}/wine/vmm.vxd
%{_libdir}/wine/vnbt.vxd
%{_libdir}/wine/vnetbios.vxd
%{_libdir}/wine/vtdapi.vxd
%{_libdir}/wine/vwin32.vxd
%{_libdir}/wine/w32skrnl.dll
%{_libdir}/wine/avifile.dll16
%{_libdir}/wine/comm.drv16
%{_libdir}/wine/commdlg.dll16
%{_libdir}/wine/compobj.dll16
%{_libdir}/wine/ctl3d.dll16
%{_libdir}/wine/ctl3dv2.dll16
%{_libdir}/wine/ddeml.dll16
%{_libdir}/wine/dispdib.dll16
%{_libdir}/wine/display.drv16
%{_libdir}/wine/gdi.exe16.so
%{_libdir}/wine/imm.dll16
%{_libdir}/wine/krnl386.exe16.so
%{_libdir}/wine/keyboard.drv16
%{_libdir}/wine/lzexpand.dll16
%{_libdir}/wine/mmsystem.dll16
%{_libdir}/wine/mouse.drv16
%{_libdir}/wine/msacm.dll16
%{_libdir}/wine/msvideo.dll16
%{_libdir}/wine/ole2.dll16
%{_libdir}/wine/ole2conv.dll16
%{_libdir}/wine/ole2disp.dll16
%{_libdir}/wine/ole2nls.dll16
%{_libdir}/wine/ole2prox.dll16
%{_libdir}/wine/ole2thk.dll16
%{_libdir}/wine/olecli.dll16
%{_libdir}/wine/olesvr.dll16
%{_libdir}/wine/rasapi16.dll16
%{_libdir}/wine/setupx.dll16
%{_libdir}/wine/shell.dll16
%{_libdir}/wine/sound.drv16
%{_libdir}/wine/storage.dll16
%{_libdir}/wine/stress.dll16
%{_libdir}/wine/system.drv16
%{_libdir}/wine/toolhelp.dll16
%{_libdir}/wine/twain.dll16
%{_libdir}/wine/typelib.dll16
%{_libdir}/wine/ver.dll16
%{_libdir}/wine/w32sys.dll16
%{_libdir}/wine/win32s16.dll16
%{_libdir}/wine/win87em.dll16
%{_libdir}/wine/winaspi.dll16.so
%{_libdir}/wine/windebug.dll16
%{_libdir}/wine/wineps16.drv16
%{_libdir}/wine/wing.dll16
%{_libdir}/wine/winhelp.exe16
%{_libdir}/wine/winnls.dll16
%{_libdir}/wine/winoldap.mod16
%{_libdir}/wine/winsock.dll16
%{_libdir}/wine/wintab.dll16
%{_libdir}/wine/wow32.dll
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/winebus.inf
%{_datadir}/wine/winehid.inf
%{_datadir}/wine/l_intl.nls

%files common
%{_bindir}/notepad
%{_bindir}/winedbg
%{_bindir}/winefile
%{_bindir}/winemine
%{_bindir}/winemaker
%{_bindir}/winepath
%{_bindir}/msiexec
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/wineboot
%{_bindir}/wineconsole
%{_bindir}/winecfg
%{_mandir}/man1/wine.1*
%{_mandir}/man1/wineserver.1*
%{_mandir}/man1/msiexec.1*
%{_mandir}/man1/notepad.1*
%{_mandir}/man1/regedit.1*
%{_mandir}/man1/regsvr32.1*
%{_mandir}/man1/wineboot.1*
%{_mandir}/man1/winecfg.1*
%{_mandir}/man1/wineconsole.1*
%{_mandir}/man1/winefile.1*
%{_mandir}/man1/winemine.1*
%{_mandir}/man1/winepath.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wine.1*
%lang(de) %{_mandir}/de.UTF-8/man1/wineserver.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wine.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/wineserver.1*
%lang(pl) %{_mandir}/pl.UTF-8/man1/wine.1*

%files fonts
# meta package

%if 0%{?wine_staging}
%files arial-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/arial*
%endif #0%{?wine_staging}

%files courier-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cou*

%files fixedsys-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/*vgafix.fon

%files system-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/cvgasys.fon
%{_datadir}/wine/fonts/hvgasys.fon
%{_datadir}/wine/fonts/jvgasys.fon
%{_datadir}/wine/fonts/svgasys.fon
%{_datadir}/wine/fonts/vgas1255.fon
%{_datadir}/wine/fonts/vgas1256.fon
%{_datadir}/wine/fonts/vgas1257.fon
%{_datadir}/wine/fonts/vgas874.fon
%{_datadir}/wine/fonts/vgasys.fon
%{_datadir}/wine/fonts/vgasyse.fon
%{_datadir}/wine/fonts/vgasysg.fon
%{_datadir}/wine/fonts/vgasysr.fon
%{_datadir}/wine/fonts/vgasyst.fon

%files small-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sma*
%{_datadir}/wine/fonts/jsma*

%files marlett-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/marlett.ttf

%files ms-sans-serif-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/sse*
%if 0%{?wine_staging}
%{_datadir}/wine/fonts/msyh.ttf
%endif

%files tahoma-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/tahoma*ttf

%files tahoma-fonts-system
%doc README-tahoma
%{_datadir}/fonts/wine-tahoma-fonts
%{_fontconfig_confdir}/20-wine-tahoma*conf
%{_fontconfig_templatedir}/20-wine-tahoma*conf

%if 0%{?wine_staging}
%files times-new-roman-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/times.ttf

%files times-new-roman-fonts-system
%{_datadir}/fonts/wine-times-new-roman-fonts
%endif

%files symbol-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/symbol.ttf

%files wingdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/wingding.ttf

%files wingdings-fonts-system
%{_datadir}/fonts/wine-wingdings-fonts

%files desktop
%{_datadir}/applications/wine-notepad.desktop
%{_datadir}/applications/wine-winefile.desktop
%{_datadir}/applications/wine-winemine.desktop
%{_datadir}/applications/wine-mime-msi.desktop
%{_datadir}/applications/wine.desktop
%{_datadir}/applications/wine-regedit.desktop
%{_datadir}/applications/wine-uninstaller.desktop
%{_datadir}/applications/wine-winecfg.desktop
%{_datadir}/applications/wine-wineboot.desktop
%{_datadir}/applications/wine-winhelp.desktop
%{_datadir}/applications/wine-wordpad.desktop
%{_datadir}/applications/wine-oleview.desktop
%{_datadir}/desktop-directories/Wine.directory
%config %{_sysconfdir}/xdg/menus/applications-merged/wine.menu
%if 0%{?fedora} >= 10
%{_datadir}/icons/hicolor/scalable/apps/*svg
%endif

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%files systemd
%config %{_binfmtdir}/wine.conf
%endif

%if 0%{?rhel} == 6
%files sysvinit
%{_initrddir}/wine
%endif

# ldap subpackage
%files ldap
%{_libdir}/wine/wldap32.dll.so

# cms subpackage
%files cms
%{_libdir}/wine/mscms.dll.so

# twain subpackage
%files twain
%{_libdir}/wine/twain_32.%{winedll}
%{_libdir}/wine/sane.ds.so

# capi subpackage
%files capi
%{_libdir}/wine/capi2032.dll.so

%files devel
%{_bindir}/function_grep.pl
%{_bindir}/widl
%{_bindir}/winebuild
%{_bindir}/winecpp
%{_bindir}/winedump
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/wmc
%{_bindir}/wrc
%{_mandir}/man1/widl.1*
%{_mandir}/man1/winebuild.1*
%{_mandir}/man1/winecpp.1*
%{_mandir}/man1/winedump.1*
%{_mandir}/man1/winegcc.1*
%{_mandir}/man1/winemaker.1*
%{_mandir}/man1/wmc.1*
%{_mandir}/man1/wrc.1*
%{_mandir}/man1/winedbg.1*
%{_mandir}/man1/wineg++.1*
%lang(de) %{_mandir}/de.UTF-8/man1/winemaker.1*
%lang(fr) %{_mandir}/fr.UTF-8/man1/winemaker.1*
%attr(0755, root, root) %dir %{_includedir}/wine
%{_includedir}/wine/*
%{_libdir}/*.so
%{_libdir}/wine/*.a
%{_libdir}/wine/*.def

%files pulseaudio
%{_libdir}/wine/winepulse.drv.so

%files alsa
%{_libdir}/wine/winealsa.drv.so

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%files openal
%{_libdir}/wine/openal32.dll.so
%endif

%if 0%{?fedora}
%files opencl
%{_libdir}/wine/opencl.dll.so
%endif

%changelog
* Mon Aug 05 2019 Michael Cronenworth <mike@cchtml.com> 4.13-2
- fix alternatives for d3d dlls

* Sun Aug 04 2019 Michael Cronenworth <mike@cchtml.com> 4.13-1
- version update
- add alternatives for d3d dlls to play with dxvk

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Michael Cronenworth <mike@cchtml.com> 4.12.1-1
- version update

* Sun Jun 23 2019 Michael Cronenworth <mike@cchtml.com> 4.11-1
- version update

* Thu Jun 13 2019 Michael Cronenworth <mike@cchtml.com> 4.10-1
- version update
- compile with MinGW support

* Sun May 26 2019 Michael Cronenworth <mike@cchtml.com> 4.9-1
- version update

* Wed May 15 2019 Michael Cronenworth <mike@cchtml.com> 4.8-2
- Fix default wine svg (RHBZ#1598994)

* Tue May 14 2019 Michael Cronenworth <mike@cchtml.com> 4.8-1
- version update

* Sun Apr 28 2019 Michael Cronenworth <mike@cchtml.com> 4.7-1
- version update

* Sun Apr 14 2019 Michael Cronenworth <mike@cchtml.com> 4.6-1
- version update

* Tue Apr 02 2019 Michael Cronenworth <mike@cchtml.com> 4.5-1
- version update

* Tue Mar 19 2019 Michael Cronenworth <mike@cchtml.com> 4.4-1
- version update

* Sun Mar 03 2019 Michael Cronenworth <mike@cchtml.com> 4.3-1
- version update

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 4.2-3
- Rebuilt against fixed atk (#1626575)

* Tue Feb 19 2019 Björn Esser <besser82@fedoraproject.org> - 4.2-2
- Fix version requirement on wine-mono

* Sun Feb 17 2019 Michael Cronenworth <mike@cchtml.com> 4.2-1
- version update

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Michael Cronenworth <mike@cchtml.com> 4.0-1
- version update

* Thu Jan 17 2019 Michael Cronenworth <mike@cchtml.com> 4.0-0.5.rc6
- version update
- Include path fix (RHBZ#1664292)

* Thu Jan 03 2019 Michael Cronenworth <mike@cchtml.com> 4.0-0.4.rc4
- version update

* Sun Dec 16 2018 Michael Cronenworth <mike@cchtml.com> 4.0-0.3.rc2
- version update

* Sat Dec 15 2018 Björn Esser <besser82@fedoraproject.org> - 4.0-0.2.rc1
- fix typos and wording in readme-files

* Mon Dec 10 2018 Michael Cronenworth <mike@cchtml.com> 4.0-0.1.rc1
- version update

* Wed Nov 28 2018 Michael Cronenworth <mike@cchtml.com> 3.21-1
- version update

* Mon Nov 12 2018 Michael Cronenworth <mike@cchtml.com> 3.20-1
- version update

* Mon Oct 29 2018 Michael Cronenworth <mike@cchtml.com> 3.19-1
- version update

* Wed Oct 17 2018 Michael Cronenworth <mike@cchtml.com> 3.18-1
- version update

* Sun Sep 30 2018 Michael Cronenworth <mike@cchtml.com> 3.17-1
- version update

* Mon Sep 17 2018 Michael Cronenworth <mike@cchtml.com> 3.16-1
- version update

* Mon Sep 03 2018 Michael Cronenworth <mike@cchtml.com> 3.15-1
- version update

* Mon Aug 20 2018 Michael Cronenworth <mike@cchtml.com> 3.14-1
- version update

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.13-5
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.13-4
- Rebuild for new binutils

* Thu Jul 26 2018 Michael Cronenworth <mike@cchtml.com> 3.13-3
- Fix application of patch

* Tue Jul 24 2018 Michael Cronenworth <mike@cchtml.com> 3.13-2
- Add patch to fix audio with staging

* Sat Jul 21 2018 Michael Cronenworth <mike@cchtml.com> 3.13-1
- version update

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Michael Cronenworth <mike@cchtml.com> 3.12-1
- version update

* Sun Jun 24 2018 Michael Cronenworth <mike@cchtml.com> 3.11-1
- version update

* Tue Jun 12 2018 Michael Cronenworth <mike@cchtml.com> 3.10-1
- version update

* Wed May 30 2018 Michael Cronenworth <mike@cchtml.com> 3.9-1
- version update

* Sat May 12 2018 Michael Cronenworth <mike@cchtml.com> 3.8-1
- version update

* Sat Apr 14 2018 Michael Cronenworth <mike@cchtml.com> 3.6-1
- version update
- enable wine-staging

* Tue Apr 03 2018 Michael Cronenworth <mike@cchtml.com> 3.5-1
- version update

* Fri Mar 16 2018 Michael Cronenworth <mike@cchtml.com> 3.4-1
- version update

* Fri Mar 02 2018 Michael Cronenworth <mike@cchtml.com> 3.3-2
- enable SDL2 and vulkan support

* Fri Mar 02 2018 Michael Cronenworth <mike@cchtml.com> 3.3-1
- version update

* Tue Feb 20 2018 Michael Cronenworth <mike@cchtml.com> 3.2-2
- fix another upgrade path from wine-staging (RHBZ#1547137)

* Mon Feb 19 2018 Michael Cronenworth <mike@cchtml.com> 3.2-1
- version update

* Wed Feb 14 2018 Michael Cronenworth <mike@cchtml.com> 3.1-2
- fix upgrade path from wine-staging

* Fri Feb 09 2018 Michael Cronenworth <mike@cchtml.com> 3.1-1
- version update
- disable wine-staging

* Sat Nov 25 2017 Michael Cronenworth <mike@cchtml.com> 2.21-1
- version update

* Mon Nov 06 2017 Michael Cronenworth <mike@cchtml.com> 2.20-1
- version update

* Sun Oct 22 2017 Michael Cronenworth <mike@cchtml.com> 2.19-1
- version update

* Wed Oct 11 2017 Michael Cronenworth <mike@cchtml.com> 2.18-1
- version update

* Thu Sep 21 2017 Michael Cronenworth <mike@cchtml.com> 2.17-1
- version update

* Thu Sep 07 2017 Michael Cronenworth <mike@cchtml.com> 2.16-1
- version update
- drop BR on ImageMagick

* Wed Aug 23 2017 Michael Cronenworth <mike@cchtml.com> 2.15-1
- version update

* Tue Aug 08 2017 Michael Cronenworth <mike@cchtml.com> 2.14-1
- version update

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Tue Jul 25 2017 Michael Cronenworth <mike@cchtml.com> 2.13-1
- version update

* Wed Jul 12 2017 Michael Cronenworth <mike@cchtml.com> 2.12-1
- version update

* Tue Jun 27 2017 Michael Cronenworth <mike@cchtml.com> 2.11-1
- version update

* Tue Jun 13 2017 Michael Cronenworth <mike@cchtml.com> 2.10-1
- version update

* Mon May 29 2017 Michael Cronenworth <mike@cchtml.com> 2.9-1
- version update

* Tue May 16 2017 Michael Cronenworth <mike@cchtml.com> 2.8-1
- version update

* Tue May 02 2017 Michael Cronenworth <mike@cchtml.com> 2.7-1
- version update

* Wed Apr 19 2017 Michael Cronenworth <mike@cchtml.com> 2.6-1
- version update

* Mon Apr 10 2017 Michael Cronenworth <mike@cchtml.com> 2.5-1
- version update

* Thu Mar 23 2017 Michael Cronenworth <mike@cchtml.com> 2.4-2
- update wine-mono requirement

* Thu Mar 23 2017 Michael Cronenworth <mike@cchtml.com> 2.4-1
- version update

* Mon Mar 06 2017 Michael Cronenworth <mike@cchtml.com> 2.3-1
- version update

* Mon Feb 20 2017 Michael Cronenworth <mike@cchtml.com> 2.2-1
- version update

* Thu Feb 09 2017 Michael Cronenworth <mike@cchtml.com> 2.1-1
- version update

* Wed Jan 25 2017 Michael Cronenworth <mike@cchtml.com> 2.0-1
- version update

* Mon Jan 23 2017 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc6
- version update

* Mon Jan 16 2017 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc5
- version update

* Mon Jan 09 2017 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc4
- version update

* Tue Dec 27 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc3
- version update

* Wed Dec 21 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc2
- version update

* Thu Dec 15 2016 Michael Cronenworth <mike@cchtml.com> 2.0-0.1.rc1
- version update

* Wed Nov 23 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-2
- drop sysvinit on Fedora, again

* Wed Nov 16 2016 Michael Cronenworth <mike@cchtml.com> 1.9.23-1
- version update
- remove old cruft in spec
- add hard cups-libs dependency (rhbz#1367537)
- include mp3 support (rhbz#1395711)

* Thu Nov 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.22-1
- version update

* Mon Oct 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.21-1
- version update

* Sun Oct 02 2016 Michael Cronenworth <mike@cchtml.com> 1.9.20-1
- version update

* Mon Sep 19 2016 Michael Cronenworth <mike@cchtml.com> 1.9.19-1
- version update

* Thu Sep 15 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.18-2
- fix aarch64 definition

* Wed Sep 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.18-1
- version update

* Sun Aug 28 2016 Michael Cronenworth <mike@cchtml.com> 1.9.17-1
- version update

* Sat Aug 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.16-2
- build on aarch64

* Tue Aug 09 2016 Michael Cronenworth <mike@cchtml.com> 1.9.16-1
- version update

* Fri Jul 29 2016 Michael Cronenworth <mike@cchtml.com> 1.9.15-1
- version update

* Mon Jul 11 2016 Michael Cronenworth <mike@cchtml.com> 1.9.14-1
- version update

* Fri Jul 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.13-1
- version update

* Wed Jun 15 2016 Michael Cronenworth <mike@cchtml.com> 1.9.12-1
- version update

* Tue Jun 07 2016 Michael Cronenworth <mike@cchtml.com> 1.9.11-1
- version update

* Tue May 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-2
- gecko update

* Tue May 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.10-1
- version upgrade

* Sun May 01 2016 Michael Cronenworth <mike@cchtml.com> 1.9.9-1
- version upgrade

* Sun Apr 17 2016 Michael Cronenworth <mike@cchtml.com> 1.9.8-1
- version upgrade

* Sun Apr 03 2016 Michael Cronenworth <mike@cchtml.com> 1.9.7-1
- version upgrade

* Mon Mar 21 2016 Michael Cronenworth <mike@cchtml.com> 1.9.6-1
- version upgrade

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-2
- update mono requirement

* Tue Mar 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.5-1
- version upgrade

* Mon Feb 22 2016 Michael Cronenworth <mike@cchtml.com> 1.9.4-1
- version upgrade

* Mon Feb 08 2016 Michael Cronenworth <mike@cchtml.com> 1.9.3-1
- version upgrade

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Michael Cronenworth <mike@cchtml.com> 1.9.2-1
- version upgrade
- enable gstreamer support

* Sun Jan 10 2016 Michael Cronenworth <mike@cchtml.com> 1.9.1-1
- version upgrade

* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> 1.9.0-1
- version upgrade

* Wed Dec 23 2015 Michael Cronenworth <mike@cchtml.com> 1.8-1
- version upgrade

* Tue Dec 15 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.2
- version upgrade, 1.8-rc4
- enabling compiler optimizations again (-O2), thanks to gcc 5.3

* Sun Dec 06 2015 Michael Cronenworth <mike@cchtml.com> 1.8-0.1
- version upgrade, 1.8-rc3

* Sun Nov 15 2015 Michael Cronenworth <mike@cchtml.com> 1.7.55-1
- version upgrade

* Wed Nov 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.54-1
- version upgrade

* Wed Oct 21 2015 Michael Cronenworth <mike@cchtml.com> 1.7.53-1
- version upgrade

* Sat Oct 03 2015 Michael Cronenworth <mike@cchtml.com> 1.7.52-1
- version upgrade

* Tue Sep 08 2015 Michael Cronenworth <mike@cchtml.com> 1.7.51-1
- version upgrade

* Mon Aug 24 2015 Michael Cronenworth <mike@cchtml.com> 1.7.50-1
- version upgrade

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-2
- backport gecko 2.40 patch

* Fri Aug 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.49-1
- version upgrade

* Mon Aug 10 2015 Björn Esser <bjoern.esser@gmail.com> - 1.7.48-2
- rebuilt for mingw-wine-gecko-2.40

* Fri Jul 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.48-1
- version upgrade

* Sun Jul 12 2015 Michael Cronenworth <mike@cchtml.com> 1.7.47-1
- version upgrade

* Mon Jun 29 2015 Michael Cronenworth <mike@cchtml.com> 1.7.46-1
- version upgrade

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 14 2015 Michael Cronenworth <mike@cchtml.com> 1.7.45-1
- version upgrade

* Sun May 31 2015 Michael Cronenworth <mike@cchtml.com> 1.7.44-1
- version upgrade

* Mon May 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.43-1
- version upgrade

* Mon May 04 2015 Michael Cronenworth <mike@cchtml.com> 1.7.42-1
- version upgrade

* Sat Apr 18 2015 Michael Cronenworth <mike@cchtml.com> 1.7.41-1
- version upgrade
- Disable gstreamer support (rhbz#1204185)

* Mon Apr 06 2015 Michael Cronenworth <mike@cchtml.com> 1.7.40-1
- version upgrade

* Sun Mar 22 2015 Michael Cronenworth <mike@cchtml.com> 1.7.39-1
- version upgrade
- Enable some optimizations and workarounds for GCC5 regressions

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 1.7.38-3
- Drop sysvinit subpackage on F23+

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-2
- Fix wine-gecko and wine-mono versions

* Sat Mar 07 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.38-1
- version upgrade

* Sun Feb 22 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.37-1
- version upgrade

* Mon Feb 16 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-2
- Patch for RtlUnwindEx fix (staging bz #68)
- Use new systemd macros for binfmt handling

* Sun Feb 08 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.36-1
- version upgrade

* Wed Feb 04 2015 Orion Poplawski <orion@cora.nwra.com> - 1.7.35-3
- Add patch to fix stack smashing (bug #1110419)

* Mon Jan 26 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-2
- Rebuild (libgphoto2)

* Sun Jan 25 2015 Michael Cronenworth <mike@cchtml.com> - 1.7.35-1
- version upgrade
- use alternatives system, remove wow sub-package

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.34-2
- Rebuild (libgphoto2)

* Sat Jan 10 2015 Michael Cronenworth <mike@cchtml.com>
- 1.7.34-1
- version upgrade
- enable OpenCL support (rhbz#1176605)

* Sun Dec 14 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.33-1
- version upgrade

* Sun Nov 30 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.32-1
- version upgrade
- wine-mono upgrade

* Fri Nov 14 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.31-1
- version upgrade
- wine-gecko upgrade
- add some missing arch requires

* Sun Nov 02 2014 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 1.7.30-1
- version upgrade (rhbz#1159548)
- use winepulse patch from compholio patchset when build w/o
  compholio (rhbz#1151862)

* Fri Oct 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.29-1
- version upgrade

* Sun Oct 05 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.28-1
- version upgrade
- New sub-package for wingdings font system integration

* Wed Sep 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.27-1
- version upgrade

* Mon Sep 08 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.26-1
- version upgrade

* Sun Aug 24 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.25-1
- version upgrade

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.24-1
- version upgrade
- No longer install Wine fonts into system directory (rhbz#1039763)

* Thu Jul 17 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-4
- prevent accidential build with compholio-patchset on EPEL
- rebuild for pulseaudio (bug #1117683)

* Mon Jul 14 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-3
- dropped virtual Provides: %%{name}(compholio)

* Sat Jul 12 2014 Björn Esser <bjoern.esser@gmail.com> - 1.7.22-2
- added conditionalized option to build with compholio-patchset for pipelight
  Source900 -- compholio-patchset, wine-arial-fonts sub-package,
  BR: libattr-devel and configure --with-xattr for Silverlight DRM-stuff

* Fri Jul 11 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.22-1
- version upgrade

* Wed Jul 09 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.21-2
- Fixes for EPEL7 (rhbz#1117422)

* Tue Jul 01 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.21-1
- version upgrade

* Thu Jun 19 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.20-1
- version upgrade

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 18 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.19-1
- version upgrade

* Sat May 10 2014 Michael Cronenworth <mike@cchtml.com>
- 1.7.18-1
- version upgrade

* Fri Apr 25 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-2
- fix systemd binfmt location (rhbz#1090170)

* Tue Apr 22 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.17-1
- version upgrade

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-2
- explicitly require libpng (fixes rhbz#1085075)

* Mon Apr 07 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.16-1
- version upgrade

* Mon Mar 24 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.15-1
- version upgrade

* Sat Mar 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.14-1
- version upgrade

* Sun Feb 23 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.13-1
- version upgrade
- upgraded winepulse

* Sat Feb 08 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.12-1
- version upgrade

* Sun Jan 26 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.11-1
- version upgrade

* Thu Jan 09 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.10-1
- version upgrade
- upgraded winepulse

* Sun Dec 08 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.8-1
- version upgrade
- wine mono 4.5.2
- upgraded winepulse

* Sat Nov 23 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.7-1
- version upgrade

* Mon Oct 28 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.5-1
- version upgrade (rhbz#1023716)
- upgraded winepulse

* Sat Oct 12 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.4-1
- version upgrade (rhbz#1018601)

* Sat Sep 28 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.3-1
- version upgrade (rhbz#1008441)
- upgraded winepulse
- wine gecko 2.24
- fix systemd subpackage scriplet (rhbz#1010742)

* Sun Sep 15 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.2-1
- version upgrade
- workaround for rhbz#968860
- upgraded winepulse

* Sat Aug 31 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.1-2
- fix icons with patch provided by Frank Dana (rhbz#997543)
- pull in mesa-dri-drivers in meta package to make direct rendering work out
  of the box (rhbz#827776)
- restart systemd binfmt handler on post/postun (rhbz#912354)
- add arabic translation to fedora desktop files provided by Mosaab Alzoubi
  (rhbz#979770)

* Sat Aug 31 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.1-1
- version upgrade
- build with lcms2

* Sat Aug 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.7.0-1
- version upgrade
- wine pulse update

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> - 1.6-2
- wine-desktop has architecture specific Requires so can not be noarch

* Sat Jul 20 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-1
- 1.6 release

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.6-0.5.rc5
- Perl 5.18 rebuild

* Fri Jul 12 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.4.rc5
- 1.6 rc5

* Sat Jun 29 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.3.rc4
- 1.6 rc4

* Thu Jun 27 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.2.rc3
- 1.6 rc3

* Sun Jun 16 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.6-0.1.rc2
- 1.6 rc2

* Thu May 30 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.31-1
- version upgrade
- upgraded winepulse
- wine gecko 2.21
- wine meta: require samba-winbind-clients for ntlm

* Tue May 14 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.30-1
- version upgrade

* Thu May 09 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.29-1
- version upgrade

* Sat Mar 30 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.27-1
- version upgrade

* Sun Mar 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.26-1
- version upgrade

* Tue Mar 05 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.25-1
- version upgrade
- now font package for wingdings family

* Mon Feb 18 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.24-1
- version upgrade

* Sun Feb 10 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.23-1
- version upgrade

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.5.22-2
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077
- Cleanup spec as per recently changed packaging guidelines
- fix bogus date changelog

* Sat Jan 19 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.22-1
- version upgrade
- upgraded winepulse
- wine gecko 1.9

* Sun Jan 06 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.21-1
- version upgrade

* Fri Dec 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.20-1
- version upgrade
- upgraded winepulse

* Sun Dec 09 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.19-1
- version upgrade
- upgraded winepulse

* Fri Nov 23 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.18-1
- version upgrade

* Mon Nov 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.17-1
- version upgrade
- upgraded winepulse

* Sun Oct 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.16-1
- version upgrade (rhbz#870611)
- wine mono 0.8
- update pulse patch
- fix midi in winepulse (rhbz#863129)
- fix dependencies for openssl (rhbz#868576)
- move wineboot.exe.so to -core instead of -wow (rhbz#842820)

* Mon Oct 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.15-1
- version upgrade
- wine gecko 1.8

* Sat Sep 29 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.14-1
- version upgrade

* Sat Sep 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.13-1
- version upgrade

* Fri Aug 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.12-1
- version upgrade

* Thu Aug 30 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.11-2
- rebuild on rawhide for fixed libOSMesa

* Sat Aug 18 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.11-1
- version upgrade
- use changed libOSMesa check from gentoo (>f18 still fails see rhbz#849405)

* Tue Jul 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.10-1
- version upgrade
- wine gecko 1.7

* Sat Jul 21 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.9-2
- isdn4linux now builds on ARM

* Wed Jul 18 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.9-1
- version upgrade
- clean up cjk patch to comply with default fonts where possible
- update fedora readme to point out required font packages per cjk locale

* Thu Jul 12 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.8-2
- bump for libgphoto2 2.5.0

* Wed Jul 04 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.8-1
- version upgrade (rhbz#834762)
- change {mingw-,}wine-mono require

* Sun Jun 24 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.7-1
- version upgrade (rhbz#834762)
- require new wine-gecko version

* Sat Jun 09 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.6-1
- version upgrade (rhbz#830424)
- split tahoma font package and add -system subpackage (rhbz#693180)

* Thu May 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.5-2
- fix description

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.5-1
- version upgrade (rhbz#817257)
- split out -filesystem and clean up -common/-core requires
- re-add winepulse driver (rhbz#821207, rhbz#783699)
- add font replacements for CJK to wine.inf and add information for cjk users
  to fedora readme (rhbz#815125, rhbz#820096)
- add support for and require wine-mono

* Mon May 14 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.4-1
- version upgrade

* Mon Apr 30 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.3-1
- version upgrade

* Sat Apr 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.2-2
- reenable xinput2 (rhbz#801436)

* Sat Apr 14 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.2-1
- version upgrade

* Sat Mar 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.1-1
- version upgrade

* Tue Mar 20 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-2
- require wine gecko from fedora mingw

* Mon Mar 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.5.0-1
- version upgrade

* Wed Mar 07 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-1
- version upgrade

* Tue Mar 06 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.8.rc6
- version upgrade

* Sat Feb 25 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.7.rc5
- version upgrade

* Tue Feb 21 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.6.rc4
- fix dependency issue (#795295)

* Sun Feb 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.5.rc4
- version upgrade

* Fri Feb 17 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.4.rc3
- version upgrade
- cleanup arm dependency fixes

* Fri Feb 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4-0.3.rc2
- Fix architecture dependencies on ARM so it installs

* Thu Feb 02 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.2.rc2
- version upgrade

* Sat Jan 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.4-0.1.rc1
- version upgrade

* Wed Jan 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.37-2
- Add initial support for wine on ARM

* Fri Jan 13 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.37-1
- version upgrade
- drop obsoleted patches

* Sat Dec 31 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.36-1
- version upgrade

* Mon Dec 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.35-1
- version upgrade

* Thu Dec 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.34-1
- version upgrade

* Sun Nov 20 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.33-1
- version upgrade(rhbz#755192)

* Sat Nov 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.32-1
- version upgrade (rhbz#745434)

* Fri Nov 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-2
- pull in correct wine-alsa arch in the pa meta package (rhbz#737431)

* Sun Oct 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.31-1
- version upgrade

* Mon Oct 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.30-1
- version upgrade

* Sat Sep 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.29-1
- version upgrade

* Sun Sep 11 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.28-1
- version upgrade
- require -alsa from -pulseaudio package for new sound api

* Mon Aug 29 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.27-1
- version upgrade
- fix epel build (rhbz#733802)

* Tue Aug 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-3
- drop pulse configure option
- fix f16 build (dbus/hal configure options)

* Mon Aug 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-2
- drop pulse patches
- make pulseaudio package meta and require alsa pa plugin
- update udisks patch

* Sun Aug 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.26-1
- version upgrade

* Fri Jul 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.25-1
- version upgrade
- remove -jack and -esd (retired upstream)
- rebase to Maarten Lankhorst's winepulse
- drop obsolete winepulse readme
- add udisks support from pending patches (winehq#21713, rhbz#712755)
- disable xinput2 (broken)

* Sun Jul 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.24-1
- version upgrade
- add sign as source10
- drop mshtml patch (upstream)

* Sun Jun 26 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.23-1
- version upgrade
- winepulse upgrade (0.40)
- fix gcc optimization problem (rhbz#710352, winehq#27375)

* Tue Jun 21 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-2
- workaround gcc optimization problem (rhbz#710352)

* Sun Jun 12 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.22-1
- version upgrade

* Sat May 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.21-1
- version upgrade

* Sun May 15 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.20-1
- version upgrade

* Sat Apr 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.19-1
- version upgrade (#701003)
- remove wine-oss
- disable hal (>=f16)

* Sat Apr 16 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.18-1
- version upgrade

* Thu Apr 07 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-3
- add fix for office installation (upstream #26650)

* Tue Apr 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-2
- cleanup spec file
- remove rpath via chrpath
- convert README files to utf8
- move SysV init script so sysvinit subpackage (>=f15)
- add some missing lsb keywords to init file
- create systemd subpackage and require it in the wine-desktop package (>=f15)
- disable embedded bitmaps in tahoma (#693180)
- provide readme how to disable wine-tahoma in fontconfig (#693180)

* Sat Apr 02 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.17-1
- version upgrade

* Fri Mar 18 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.16-1
- version upgrade
- cleanup unneeded patches
- drop some patches
- reenable smp build

* Thu Mar 17 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-3
- reenable fonts

* Sun Mar 13 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-2
- use svg files for icons (#684277)

* Tue Mar 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.15-1
- version upgrade

* Tue Mar 01 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-2
- prepare for wine-gecko

* Sat Feb 19 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.14-1
- version upgrade

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.13-1
- version upgrade
- update desktop files

* Mon Jan 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.12-1
- version upgrade

* Sun Jan 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.11-1
- version upgrade

* Tue Dec 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.10-1
- version upgrade

* Sat Dec 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.9-1
- version upgrade

* Sat Nov 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.8-1
- version upgrade
- require libXcursor (#655255)
- require wine-openal in wine meta package (#657144)

* Tue Nov 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-2
- cleanup cflags a bit

* Sat Nov 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.7-1
- version upgrade
- fix package description (#652718)
- compile with D_FORTIFY_SOURCE=0 for now to avoid breaking wine (#650875)

* Fri Oct 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.6-1
- version upgrade
- rebase winepulse configure patch
- add gstreamer BR for new gstreamer support
- add libtiff BR for new tiff support

* Mon Oct 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.5-1
- version upgrade

* Sun Oct 03 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.4-1
- version upgrade

* Wed Sep 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-2
- winepulse upgrade (0.39)

* Mon Sep 20 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.3-1
- version upgrade

* Wed Sep 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.2-1
- version upgrade

* Sat Aug 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.1-1
- version ugprade

* Sat Jul 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.3.0-1
- version upgrade

* Wed Jul 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2.0-2
- fix segfault (#617968)
- enable openal-soft on el6

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-1
- final release

* Fri Jul 16 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.8.rc7
- improve font patch

* Sun Jul 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.7.rc7
- version upgrade
- make sure font packages include the license file in case they are installed
  standalone

* Sun Jul 04 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.6.rc6
- version upgrade
- use new winelogo from user32
- winepulse upgrade

* Sun Jun 27 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.5.rc5
- version upgrade
- require liberation-narrow-fonts

* Fri Jun 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.4.rc4
- version upgrade
- fixes winecfg on 64bit (#541986)
- require wine-common from -core to ensure man pages and wine.inf are present
  (#528335)

* Sun Jun 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.3.rc3
- version upgrade

* Mon May 31 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.2.rc2
- version upgrade

* Mon May 24 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.2-0.1.rc1
- upgrade to rc1
- add BR for ImageMagick and icoutils
- spec cleanup
- install available icon files (#594950)
- desktop package requires wine x86-32 because of wine/wine64 rename
- put system/small fonts in right place

* Wed May 19 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-5
- fix font issues

* Thu May 13 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-4
- fix install of 32bit only wine on x86_64 via install wine.i686

* Wed May 12 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-3
- move wine symlink to -wow for 32bit (#591690)

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-2
- fix manpage conflict between -common and -devel

* Sun May 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.44-1
- version upgrade (#580024)

* Sun Apr 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.43-1
- version upgrade

* Sun Apr 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.42-1
- version upgrade
- rework for wow64

* Mon Mar 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-3
- add support for mingw32-wine-gecko

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-2
- convert to font package guidelines
- add libv4l-devel BR

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.41-1
- version upgrade (#577587, #576607)
- winepulse upgrade (0.36)

* Sat Mar 06 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.40-1
- version upgrade

* Sun Feb 21 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.39-1
- version upgrade

* Tue Feb 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.38-1
- version upgrade
- winepulse upgrade (0.35)

* Mon Jan 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.36-1
- version upgrade (#554102)
- require -common in -desktop (#549190)

* Sat Dec 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.35-1
- version upgrade

* Fri Dec 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.34-1
- version upgrade (#546749)

* Mon Nov 16 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.33-1
- version upgrade
- winepulse update (.33)
- require gnutls (#538694)
- use separate WINEPREFIX on x86_64 per default (workaround for #533806)
- drop explicit xmessage require (#537610)

* Tue Oct 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.32-1
- version upgrade (#531358)
- update winepulse

* Mon Sep 28 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.30-1
- version upgrade
- openal support
- drop steam regression patch

* Sun Sep 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-3
- patch for steam regression (upstream #19916)
- update winepulse winecfg patch

* Thu Sep 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-2
- rebuild for new gcc (#505862)

* Wed Sep 02 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.29-1
- version upgrade

* Mon Aug 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.28-1
- version upgrade
- make 32bit and 64bit version parallel installable

* Sun Aug 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.27-1
- version upgrade
- WinePulse 0.30

* Thu Aug 06 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-2
- build 32bit wine on x86_64 and prepare for 64bit parallel build (#487651)
- fix subpackage problems (#485410,#508766,#508944,#514967)
- fix nss dependencies on x86_64 (#508412)

* Sat Jul 18 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.26-1
- version upgrade
- WinePulse 0.29
- require Xrender isa for x86_64 (#510947)

* Thu Jul 09 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.25-1
- version upgrade (#509648)

* Mon Jun 29 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-3
- pull in nss correctly on x86_64

* Sun Jun 21 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-2
- adjust wine-menu to follow wine behavior (wine-wine instead of Wine)
  (fixes #479649, #495953)
- fix wine help desktop entry (#495953, #507154)
- add some more wine application desktop entries (#495953)
- split alsa/oss support into wine-alsa/wine-oss
- drop nas require from wine meta package
- fix dns resolution (#492700)

* Fri Jun 19 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.24-1
- version upgrade
- WinePulse 0.28
- drop meta package requires for jack and esd (#492983)

* Wed Jun 10 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.23-1
- version upgrade (#491321)
- rediff pulseaudio patch (Michael Cronenworth)

* Wed May 13 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-2
- fix uninstaller (#500479)

* Tue May 12 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.21-1
- version upgrade

* Mon Apr 27 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.20-1
- version upgrade

* Mon Mar 30 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.18-1
- version upgrade (#490672, #491321)
- winepulse update

* Sun Mar 15 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net> - 1.1.15-3
— Make sure F11 font packages have been built with F11 fontforge

* Tue Feb 24 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-2
- switch from i386 to ix86

* Sun Feb 15 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.15-1
- version upgrade
- new pulse patches

* Sat Jan 31 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.14-1
- version upgrade

* Sat Jan 17 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.13-1
- version upgrade
- fix gcc compile problems (#440139, #461720)

* Mon Jan 05 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.12-1
- version upgrade

* Sat Dec 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.10-1
- version upgrade
- add native pulseaudio driver from winehq bugzilla (#10495)
  fixes #474435, #344281

* Mon Nov 24 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-2
- fix #469907

* Sun Nov 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.9-1
- version upgrade

* Sun Oct 26 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.7-1
- version upgrade

* Thu Oct 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.6-1
- version upgrade
- fix multiarch problems (#466892,#467480)

* Sat Sep 20 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.5-1
- version upgrade

* Fri Sep 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.4-1
- version upgrade
- drop wine-prefixfonts.patch (#460745)

* Fri Aug 29 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.3-1
- version upgrade

* Sun Jul 27 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.2-1
- version upgrade (#455960, #456831)
- require freetype (#452417)
- disable wineprefixcreate patch for now

* Fri Jul 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.1.1-1
- version upgrade

* Tue Jun 17 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-1
- version upgrade (#446311,#417161)
- fix wine.desktop mime types (#448338)
- add desktop package including desktop files and binary handler (#441310)
- pull in some wine alsa/pulseaudio patches (#344281)

* Mon Jun 16 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.5.rc5
- version upgrade

* Fri Jun 06 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.4.rc4
- version upgrade

* Sun Jun 01 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.3.rc3
- version upgrade

* Fri May 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.2.rc2
- version upgrade
- add compile workaround for fedora 9/rawhide (#440139)

* Sat May 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 1.0-0.1.rc1
- version upgrade to rc1

* Mon May 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.61-1
- version upgrade

* Fri Apr 18 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.60-1
- version upgrade

* Sat Apr 05 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.59-1
- version upgrade

* Sat Mar 22 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.58-1
- version upgrade

* Tue Mar 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.57-1
- version upgrade

* Sat Feb 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.56-1
- version upgrade

* Sun Feb 10 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.55-1
- version upgrade

* Fri Jan 25 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.54-1
- version upgrade
- remove default pulseaudio workaround (#429420,#428745)
- improve pulseaudio readme

* Sun Jan 13 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-2
- add some missing BR

* Sat Jan 12 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.53-1
- version upgrade

* Sat Dec 29 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-2
- fix menu bug (#393641)

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.52-1
- version upgrade

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-3
- add -n Wine to pulseaudio workaround
- try to fix menu bug #393641

* Fri Dec 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-2
- add fix for #344281 pulseaudio workaround
- fix #253474: wine-jack should require jack-audio-connection-kit

* Sun Dec 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.51-1
- version upgrade

* Sat Dec 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.50-1
- version upgrade

* Tue Nov 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.49-1
- version upgrade

* Fri Oct 26 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.48-1
- version upgrade

* Sat Oct 13 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.47-1
- version upgrade

* Sun Oct 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.46-1
- version upgrade

* Sun Sep 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.45-1
- version upgrade

* Sat Aug 25 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.44-1
- version upgrade

* Sat Aug 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-2
- fix license
- fix #248999

* Sat Aug 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.43-1
- version upgrade
- fix init-script output (#252144)
- add lsb stuff (#247096)

* Sat Jul 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.42-1
- version upgrade

* Mon Jul 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.41-1
- version upgrade

* Tue Jul 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.40-1
- version upgrade

* Mon Jun 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-2
- fix desktop entries

* Sun Jun 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.9.39-1
- version upgrade
- convert to utf8 (#244046)
- fix mime entry (#243511)

* Wed Jun 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-3
- fix description

* Sun Jun 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-2
- allow full opt flags again
- set ExclusiveArch to i386 for koji to only build i386

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.38-1
- version upgrade (#242087)
- fix menu problem (#220723)
- fix BR
- clean up desktop file section

* Wed May 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.37-1
- version upgrade
- add BR for xcursor (#240648)
- add desktop entry for wineboot (#240683)
- add mime handler for msi files (#240682)
- minor cleanups

* Wed May 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-2
- fix BR (#238774)
- fix some typos

* Sat Apr 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.36-1
- version upgrade

* Mon Apr 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.35-1
- version upgrade (#234766)
- sources file comments (#235232)
- smpflags work again (mentioned by Marcin Zajączkowski)
- drop arts sound driver package, as it is no longer part of wine

* Sun Apr 01 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.34-1
- version upgrade

* Sat Mar 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.33-1
- version upgrade

* Sun Mar 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.32-1
- version upgrade

* Sat Feb 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.31-1
- version upgrade

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.30-1
- version upgrade

* Thu Jan 11 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.29-1
- version upgrade

* Mon Dec 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.27-1
- version upgrade (#220130)
- fix submenus (#216076)
- fix BR (#217338)

* Thu Nov 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.25-1
- version upgrade
- fix init script (#213230)
- fix twain subpackage content (#213396)
- create wine submenu (#205024)

* Sat Oct 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.24-1
- version upgrade

* Tue Oct 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.23-1
- version upgrade

* Sat Sep 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.22-1
- version upgrade

* Sun Sep 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.21-1
- version upgrade
- own datadir/wine (#206403)
- do not include huge changelogs (#204302)

* Mon Aug 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.20-1
- version upgrade

* Mon Aug 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.19-1
- version upgrade

* Thu Aug 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.18-1
- version upgrade

* Mon Jul 10 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.17-1
- version upgrade

* Thu Jun 29 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.16-1
- version upgrade
- rename wine to wine-core
- add meta package wine

* Fri Jun 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.15-1
- version upgrade

* Tue May 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.14-1
- version upgrade

* Fri May 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-2
- enable dbus/hal support

* Mon May 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.13-1
- version upgrade

* Sat Apr 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.12-1
- fix rpath issues (#187429,#188905)
- version upgrade

* Mon Apr 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.11-1
- version upgrade
- fix #187546

* Mon Mar 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-2
- bump for x86_64 tree inclusion \o/

* Thu Mar 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.10-1
- version upgrade
- drop ancient extra fonts

* Fri Mar 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.9-1
- version upgrade

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.8-1
- version upgrade

* Thu Feb 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-3
- fix up tarball

* Wed Feb 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-2
- fix up post/preun scriplets (#178954)

* Thu Feb 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.7-1
- version upgrade

* Thu Jan 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.6-1
- version upgrade
- drop wmf exploit patch (part of current version)

* Sun Jan 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-2
- fix for CVE-2005-4560

* Fri Jan 06 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.5-1
- version upgrade
- fix #177089 (winemine desktop entry should be in Game not in System)
- fix cflags for compile
- test new BR

* Wed Jan 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-5
- fix #176834

* Mon Jan 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-4
- add dist

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-3
- use ExclusiveArch instead of ExcludeArch

* Sun Jan 01 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-2
- own font directory
- fix devel summary
- add ExcludeArch x86_64 for now

* Sat Dec 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.4-1
- version upgrade
- changed wine.init perissions to 0644
- added autoconf BR

* Mon Dec 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.3-1
- version upgrade

* Thu Nov 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.2-1
- version upgrade

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de
0.9.1-3
- fix typo in winefile desktop file
- drop in ld config instead of editing ld.so.conf

* Sun Nov 13 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-2
- add fontforge BR and include generated fonts...

* Sat Nov 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9.1-1
- version upgrade
- move uninstaller and winecfg into wine main package...
- drop wine suite

* Sat Oct 29 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-3
- s/libwine/wine/

* Thu Oct 27 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-2
- remerge some subpackages which should be defaults

* Tue Oct 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.9-1
- upgrade to new version
- start splitting

* Mon Oct 24 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.0-1.20050930
- add fedora readme
- switch to new (old) versioning sheme

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-3
- add desktop files
- revisit summary and description
- consistant use of %%{buildroot}

* Sat Oct 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-2
- some more spec tuneups...

* Sat Oct 01 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050930-1
- version upgrade

* Sun Sep 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050925-1
- upgrade to current cvs

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050830-1
- version upgrade

* Mon Sep 19 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
20050524-2
- fedorarized version

* Mon May 30 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050524-1fc3
- Update to 20050524
- Remove pdf documentation build as it's no more included in the main archive
- Workaround for generic.ppd installation

* Tue Apr 19 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050419-1fc3
- Update to 20050419

* Thu Mar 10 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050310-1fc3
- Update to 20050310

* Sat Feb 12 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050211-1fc3
- Update to 20050211

* Tue Jan 11 2005 Vincent Béron <vberon@mecano.gme.usherb.ca> 20050111-1fc3
- Update to 20050111

* Wed Dec 1 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041201-1fc3
- Recompile for FC3
- Update to 20041201
- Small reorganization:
    - use the generic ICU static libs name;
    - no more wine group;
    - use Wine's generated stdole32.tlb file;
    - use Wine's generated fonts.

* Wed Oct 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20041019-1fc2
- Update to 20041019

* Wed Sep 15 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040914-1fc2
- Update to 20040914

* Sat Aug 14 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040813-1fc2
- Update to 20040813

* Sat Jul 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040716-1fc2
- Update to 20040716

* Fri Jun 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc2
- Recompile for FC2
- Backport from current CVS some fixes to the preloader to prevent
  a segfault on startup
- Include a currently uncommitted patch from Alexandre Julliard regarding
  further issues with the preloader

* Sun Jun 20 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040615-1fc1
- Update to 20040615
- Use of wineprefixcreate instead of old RedHat patches

* Wed May 5 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040505-1fc1
- Update to 20040505

* Fri Apr 9 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040408-1fc1
- Update to 20040408
- Change the handling of paths to DOS drives in the installation process

* Wed Mar 17 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040309-1fc1
- Update to 20040309
- Replaced winedefault.reg by wine.inf

* Wed Feb 18 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040213-1fc1
- Update to 20040213
- Moved Wine dlls back to %%{_libdir}/wine rather than %%{_libdir}/wine/wine

* Sun Jan 25 2004 Vincent Béron <vberon@mecano.gme.usherb.ca> 20040121-fc1
- Update to 20040121

* Sat Dec 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031212-fc1
- Update to 20031212

* Tue Nov 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031118-fc1
- Update to 20031118

* Thu Oct 16 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20031016-1rh9
- Update to 20031016

* Thu Sep 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030911-1rh9
- Fix of include location
- Better separation of run-time and development files
- Update to 20030911

* Wed Aug 13 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030813-1rh9
- Update to 20030813

* Wed Jul 09 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030709-1rh9
- Update to 20030709

* Wed Jun 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030618-1rh9
- Change the default C drive to ~/.wine/c, copied from /usr/share/wine
  if non-existant (Thanks to Rudolf Kastl)
- Updated to 20030618

* Tue May 20 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1rh9
- Adapted for RH9

* Thu May 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030508-1
- Add libraries definition files to devel package
- Update to 20030508

* Tue Apr 08 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030408-1
- Update to 20030408

* Tue Mar 18 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030318-1
- Update to 20030318

* Tue Mar 11 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-2
- Fix the symlinks in wine-c.

* Wed Feb 19 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030219-1
- Update to 20030129
- Various fixes in RPM build process

* Fri Jan 17 2003 Vincent Béron <vberon@mecano.gme.usherb.ca> 20030115-1
- Update to 20030115
- fix to build problem

* Thu Nov  7 2002 Vincent Béron <vberon@mecano.gme.usherb.ca> 20021031-1
- Update to 20021031
- Tweaks here and there

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 20020605-2
- fix docs (#72923)

* Wed Jul 10 2002 Karsten Hopp <karsten@redhat.de> 20020605-1
- update
- remove obsolete part of redhat patch
- redo destdir patch
- redo kde patch
- redo defaultversion patch
- fix 'my_perl unknown' error
- work around name conflict with textutils 'expand'

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020327-1
- Fix wineshelllink (#61761)
- Fix up initscript (#53625)
- Clean up spec file
- Default to emulating Windoze ME rather than 3.1, nobody uses 3.1
  applications anymore
- Auto-generate default config if none exists (#61920)

* Mon Mar 04 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020304-1
- Assign gid 66 (closest to 666 [Microsoft number] we can get for a
  system account ;) )
- Don't use glibc private functions (__libc_fork)
- Update

* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020226-1
- Fix bug #60250
- Update

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020221-1
- Update
- Don't try to launch winesetup in winelauncher, we aren't shipping it
  (#59621)

* Sun Jan 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 20020127-1
- Update
- Fix build in current environment

* Wed Aug 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010822-1
- Make sure the package can be cleanly uninstalled (#52007)
- Add build dependencies

* Thu Jul 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010726-1
- Fix -devel package group (#49989)
- remove internal CVS files
- chkconfig deletion should be in %%preun, not %%postun
- rename initscript ("Starting windows:" at startup does look off)

* Thu May 03 2001 Bernhard Rosenkraenzer <bero@redhat.com> 20010503-1
- Update
- generate HTML documentation rather than shipping plain docbook text
  (#38453)

* Sat Apr 14 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Update registry to mount "/" as drive "Z:", fixes winedbg (needs to be
  accessible from 'doze drives)
- Don't create KDE 1.x style desktop entries in wineshelllink
- Be more tolerant on failing stuff in %%post

* Thu Mar  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update

* Thu Feb 15 2001 Tim Powers <timp@redhat.com>
- fixed time.h build problems

* Wed Jan 31 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add a patch to handle .exe and .com file permissions the way we want them

* Thu Jan 18 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Restore wine's ability to use a global config file, it was removed
  in CVS for whatever reason
- Move libraries to %%{_libdir}/wine to prevent conflicts with libuser
  (Bug #24202)
- Move include files to /usr/include/wine to prevent it from messing with
  some autoconf scripts (some broken scripts assume they're running on windoze
  if /usr/include/windows.h exists...)

* Tue Dec 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix %%pre and %%postun scripts
- --enable-opengl, glibc 2.2 should be safe
- Update CVS

* Mon Nov 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update CVS
- Add a new (user) group wine that can write to the "C: drive"
  %%{_datadir}/wine-c
- Fix up winedbg installation (registry entries)
- Add "Program Files/Common Files" subdirectory to the "C: drive", it's
  referenced in the registry

* Wed Oct 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update

* Mon Aug 7 2000 Tim Powers <timp@redhat.com>
- rebuilt with new DGA

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- new snapshot
- fix compilation with gcc 2.96

* Fri Jul 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Move init script back
- new version
- move man pages to FHS locations

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- move initscript
- new snapshot

* Fri Jun 23 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Start the initscript on startup

* Tue May  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- New version
- new feature: You can now launch wine by just running a windows .exe file
  (./some.exe or just click on it in kfm, gmc and the likes)
- some spec file modifications

* Sun Feb 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- newer version
- Improve the system.ini file - all multimedia stuff should work now.

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- enable and fix up the urlmon/wininet patch
- add: autoexec.bat, config.sys, windows/win.ini windows/system.ini
  windows/Profiles/Administrator
- allow i[456]86 arches
- add some system.ini configuration

* Wed Feb  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update current
- add urlmon and wininet patches from Corel (don't apply them for now though)
- create empty shell*dll and winsock*dll files (as mentioned in the HOWTO)

* Mon Jan 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- update to current (lots of important fixes)
- Fix up the default wine.conf file (We really don't want it to look
  for CD-ROMs in /cdrom!)
- create a "root filesystem" with everything required to run wine without
  windows in %%{_datadir}/wine-c (drive c:)
- add RedHat file in /usr/doc/wine-%%{version} explaining the new directory
  layout
- wine-devel requires wine

* Tue Dec 14 1999 Preston Brown <pbrown@redhat.com>
- updated source for Powertools 6.2
- better files list

* Fri Jul 23 1999 Tim Powers <timp@redhat.com>
- updated source
- built for 6.1

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated package and spec file

* Mon Oct 26 1998 Preston Brown <pbrown@redhat.com>
- updated to 10/25/98 version.  There is really no point in keeping the
- older one, it is full of bugs and the newer one has fewer.
- commented out building of texinfo manual, it is horrendously broken.

* Mon Oct 12 1998 Michael Maher <mike@redhat.com>
- built package for 5.2
- pressured by QA, not updating.

* Fri May 22 1998 Cristian Gafton <gafton@redhat.com>
- repackaged for PowerTools
