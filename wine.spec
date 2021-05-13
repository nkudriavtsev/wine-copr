# Compiling the preloader fails with hardening enabled
%undefine _hardened_build

%global no64bit   0
%global winegecko 2.47.2
%global winemono  6.1.1
#global _default_patch_fuzz 2
%ifarch %{ix86} x86_64
%global wineacm acm
%global wineax  ax
%global winecom com
%global winecpl cpl
%global winedll dll
%global winedrv drv
%global wineds ds
%global wineexe exe
%global wineocx ocx
%global winesys sys
%global winetlb tlb
%else
%global wineacm acm.so
%global wineax  ax.so
%global winecom com.so
%global winecpl cpl.so
%global winedll dll.so
%global winedrv drv.so
%global wineds ds.so
%global wineexe exe.so
%global wineocx ocx.so
%global winesys sys.so
%global winetlb tlb.so
%endif
%ifarch %{ix86}
%global winepedir i386-windows
%global winesodir i386-unix
%endif
%ifarch x86_64
%global winepedir x86_64-windows
%global winesodir x86_64-unix
%endif
%ifarch %{arm}
%global winepedir arm-windows
%global winesodir arm-unix
%endif
%ifarch aarch64
%global winepedir aarch64-windows
%global winesodir aarch64-unix
%endif

# build with wine-staging patches, see:  https://github.com/wine-staging/wine-staging
%if 0%{?fedora}
%global wine_staging 1
%endif
# 0%%{?fedora}

# binfmt macros for RHEL
%if 0%{?rhel} == 7
%global _binfmtdir /usr/lib/binfmt.d
%global binfmt_apply() \
/usr/lib/systemd/systemd-binfmt  %{?*} >/dev/null 2>&1 || : \
%{nil}
%endif

Name:           wine
Version:        6.8
Release:        1%{?dist}
Summary:        A compatibility layer for windows applications

License:        LGPLv2+
URL:            https://www.winehq.org/
Source0:        https://dl.winehq.org/wine/source/6.x/wine-%{version}.tar.xz
Source10:       https://dl.winehq.org/wine/source/6.x/wine-%{version}.tar.xz.sign

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

# AppData files
Source150:      wine.appdata.xml

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
BuildRequires:  make
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
%if 0%{?fedora} && 0%{?fedora} <= 30
BuildRequires:  isdn4k-utils-devel
%endif
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
BuildRequires:  libvkd3d-shader-devel
BuildRequires:  vulkan-devel
BuildRequires:  libFAudio-devel
BuildRequires:  libappstream-glib

# Silverlight DRM-stuff needs XATTR enabled.
%if 0%{?wine_staging}
BuildRequires:  gtk3-devel
BuildRequires:  libattr-devel
BuildRequires:  libva-devel
%endif
# 0%%{?wine_staging}

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
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-32)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-32)
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
%if 0%{?fedora} >= 33
Recommends:     wine-dxvk(x86-64)
Recommends:     dosbox-staging
%endif
Recommends:     gstreamer1-plugins-good(x86-64)
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
Requires:       (nss-mdns(x86-32) if nss-mdns(x86-64))
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
Requires:       (nss-mdns(x86-64) if nss-mdns(x86-32))
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
%else
# 0%%{?wine_staging}
Obsoletes:     wine-arial-fonts <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
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
%else
# 0%%{?wine_staging}
Obsoletes:     wine-times-new-roman-fonts <= %{version}-%{release}
Obsoletes:     wine-times-new-roman-fonts-system <= %{version}-%{release}
%endif
# 0%%{?wine_staging}
Requires:      wine-symbol-fonts = %{version}-%{release}
Requires:      wine-webdings-fonts = %{version}-%{release}
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
%endif
# 0%%{?wine_staging}

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

%package webdings-fonts
Summary:       Wine Webdings font family
BuildArch:     noarch
Requires:      fontpackages-filesystem

%description webdings-fonts
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
%if 0%{?fedora} <= 30
%ifarch x86_64
Requires:       isdn4k-utils(x86-64)
%endif
%ifarch %{ix86}
Requires:       isdn4k-utils(x86-32)
%endif
%ifarch %{arm} aarch64
Requires:       isdn4k-utils
%endif
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

patches/patchinstall.sh DESTDIR="`pwd`" --all

# fix parallelized build
sed -i -e 's!^loader server: libs/port libs/wine tools.*!& include!' Makefile.in

%endif
# 0%%{?wine_staging}

%build
# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

# disable fortify as it breaks wine
# http://bugs.winehq.org/show_bug.cgi?id=24606
# http://bugs.winehq.org/show_bug.cgi?id=25073
export CFLAGS="`echo $RPM_OPT_FLAGS | sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//'` -Wno-error"

%ifarch aarch64
%if 0%{?fedora} >= 33
%global toolchain clang
%else
# ARM64 now requires clang
# https://source.winehq.org/git/wine.git/commit/8fb8cc03c3edb599dd98f369e14a08f899cbff95
export CC="/usr/bin/clang"
# Fedora's default compiler flags now conflict with what clang supports
# https://bugzilla.redhat.com/show_bug.cgi?id=1658311
export CFLAGS="`echo $CFLAGS | sed -e 's/-fstack-clash-protection//'`"
%endif
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
# do not ship typelibs in 32-bit packages
# https://www.winehq.org/pipermail/wine-devel/2020-June/167283.html
rm %{buildroot}%{_includedir}/wine/windows/*.tlb
%endif
%ifnarch %{arm} aarch64 x86_64
mv %{buildroot}%{_bindir}/wine-preloader %{buildroot}%{_bindir}/wine32-preloader
%endif
touch %{buildroot}%{_bindir}/wine
%ifnarch %{arm}
touch %{buildroot}%{_bindir}/wine-preloader
%endif
touch %{buildroot}%{_bindir}/wineserver
mv %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-dxgi.%{winedll}
mv %{buildroot}%{_libdir}/wine/%{winesodir}/dxgi.dll.so %{buildroot}%{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d9.%{winedll}
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10.%{winedll}
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10_1.%{winedll}
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d10core.%{winedll}
mv %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.%{winedll} %{buildroot}%{_libdir}/wine/%{winepedir}/wine-d3d11.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winepedir}/dxgi.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winesodir}/dxgi.dll.so
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d9.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10_1.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d10core.%{winedll}
touch %{buildroot}%{_libdir}/wine/%{winepedir}/d3d11.%{winedll}

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

# install and validate AppData file
mkdir -p %{buildroot}/%{_metainfodir}/
install -p -m 0644 %{SOURCE150} %{buildroot}/%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml


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
# handle upgrades for a few package updates
%{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/wine-dxgi.dll.so
%{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/wine-d3d9.%{winedll}
%{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/wine-d3d10.%{winedll}
%{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/wine-d3d11.%{winedll}
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
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/dxgi.%{winedll} \
  'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.%{winedll} 10 \
  --slave  %{_libdir}/wine/%{winesodir}/dxgi.dll.so 'wine-dxgi-so%{?_isa}' %{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d9.%{winedll} \
  'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.%{winedll} 10
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d10.%{winedll} \
  'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.%{winedll} 10 \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10_1.%{winedll} 'wine-d3d10_1%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10_1.%{winedll} \
  --slave  %{_libdir}/wine/%{winepedir}/d3d10core.%{winedll} 'wine-d3d10core%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10core.%{winedll}
%{_sbindir}/alternatives --install %{_libdir}/wine/%{winepedir}/d3d11.%{winedll} \
  'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.%{winedll} 10

%postun core
%{?ldconfig}
if [ $1 -eq 0 ] ; then
%ifarch x86_64 aarch64
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine64
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver64
%else
  %{_sbindir}/alternatives --remove wine %{_bindir}/wine32
  %{_sbindir}/alternatives --remove wineserver %{_bindir}/wineserver32
%endif
  %{_sbindir}/alternatives --remove 'wine-dxgi%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-dxgi.%{winedll}
  %{_sbindir}/alternatives --remove 'wine-d3d9%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d9.%{winedll}
  %{_sbindir}/alternatives --remove 'wine-d3d10%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d10.%{winedll}
  %{_sbindir}/alternatives --remove 'wine-d3d11%{?_isa}' %{_libdir}/wine/%{winepedir}/wine-d3d11.%{winedll}
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
%endif
%{_bindir}/winedump
%{_libdir}/wine/%{winepedir}/explorer.%{wineexe}
%{_libdir}/wine/%{winepedir}/cabarc.%{wineexe}
%{_libdir}/wine/%{winepedir}/control.%{wineexe}
%{_libdir}/wine/%{winepedir}/cmd.%{wineexe}
%{_libdir}/wine/%{winepedir}/dxdiag.%{wineexe}
%{_libdir}/wine/%{winepedir}/notepad.%{wineexe}
%{_libdir}/wine/%{winepedir}/plugplay.%{wineexe}
%{_libdir}/wine/%{winepedir}/progman.%{wineexe}
%{_libdir}/wine/%{winepedir}/taskmgr.%{wineexe}
%{_libdir}/wine/%{winepedir}/winedbg.%{wineexe}
%{_libdir}/wine/%{winesodir}/winedbg.exe.so
%{_libdir}/wine/%{winepedir}/winefile.%{wineexe}
%{_libdir}/wine/%{winepedir}/winemine.%{wineexe}
%{_libdir}/wine/%{winepedir}/winemsibuilder.%{wineexe}
%{_libdir}/wine/%{winepedir}/winepath.%{wineexe}
%{_libdir}/wine/%{winepedir}/winmgmt.%{wineexe}
%{_libdir}/wine/%{winepedir}/winver.%{wineexe}
%{_libdir}/wine/%{winepedir}/wordpad.%{wineexe}
%{_libdir}/wine/%{winepedir}/write.%{wineexe}
%{_libdir}/wine/%{winepedir}/wusa.%{wineexe}

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

%{_libdir}/wine/%{winepedir}/attrib.%{wineexe}
%{_libdir}/wine/%{winepedir}/arp.%{wineexe}
%{_libdir}/wine/%{winepedir}/aspnet_regiis.%{wineexe}
%{_libdir}/wine/%{winepedir}/cacls.%{wineexe}
%{_libdir}/wine/%{winepedir}/conhost.%{wineexe}
%{_libdir}/wine/%{winepedir}/cscript.%{wineexe}
%{_libdir}/wine/%{winepedir}/dism.%{wineexe}
%{_libdir}/wine/%{winepedir}/dplaysvr.%{wineexe}
%{_libdir}/wine/%{winepedir}/dpnsvr.%{wineexe}
%{_libdir}/wine/%{winepedir}/dpvsetup.%{wineexe}
%{_libdir}/wine/%{winepedir}/eject.%{wineexe}
%{_libdir}/wine/%{winepedir}/expand.%{wineexe}
%{_libdir}/wine/%{winepedir}/extrac32.%{wineexe}
%{_libdir}/wine/%{winepedir}/fc.%{wineexe}
%{_libdir}/wine/%{winepedir}/find.%{wineexe}
%{_libdir}/wine/%{winepedir}/findstr.%{wineexe}
%{_libdir}/wine/%{winepedir}/fsutil.%{wineexe}
%{_libdir}/wine/%{winepedir}/hostname.%{wineexe}
%{_libdir}/wine/%{winepedir}/ipconfig.%{wineexe}
%{_libdir}/wine/%{winepedir}/winhlp32.%{wineexe}
%{_libdir}/wine/%{winepedir}/mshta.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/msidb.%{wineexe}
%endif
%{_libdir}/wine/%{winepedir}/msiexec.%{wineexe}
%{_libdir}/wine/%{winepedir}/net.%{wineexe}
%{_libdir}/wine/%{winepedir}/netstat.%{wineexe}
%{_libdir}/wine/%{winepedir}/ngen.%{wineexe}
%{_libdir}/wine/%{winepedir}/ntoskrnl.%{wineexe}
%{_libdir}/wine/%{winepedir}/oleview.%{wineexe}
%{_libdir}/wine/%{winepedir}/ping.%{wineexe}
%{_libdir}/wine/%{winepedir}/powershell.%{wineexe}
%{_libdir}/wine/%{winepedir}/reg.%{wineexe}
%{_libdir}/wine/%{winepedir}/regasm.%{wineexe}
%{_libdir}/wine/%{winepedir}/regedit.%{wineexe}
%{_libdir}/wine/%{winepedir}/regsvcs.%{wineexe}
%{_libdir}/wine/%{winepedir}/regsvr32.%{wineexe}
%{_libdir}/wine/%{winepedir}/rpcss.%{wineexe}
%{_libdir}/wine/%{winepedir}/rundll32.%{wineexe}
%{_libdir}/wine/%{winepedir}/schtasks.%{wineexe}
%{_libdir}/wine/%{winepedir}/sdbinst.%{wineexe}
%{_libdir}/wine/%{winepedir}/secedit.%{wineexe}
%{_libdir}/wine/%{winepedir}/servicemodelreg.%{wineexe}
%{_libdir}/wine/%{winepedir}/services.%{wineexe}
%{_libdir}/wine/%{winepedir}/start.%{wineexe}
%{_libdir}/wine/%{winepedir}/tasklist.%{wineexe}
%{_libdir}/wine/%{winepedir}/termsv.%{wineexe}
%{_libdir}/wine/%{winepedir}/view.%{wineexe}
%{_libdir}/wine/%{winepedir}/wevtutil.%{wineexe}
%{_libdir}/wine/%{winepedir}/where.%{wineexe}
%{_libdir}/wine/%{winepedir}/whoami.%{wineexe}
%{_libdir}/wine/%{winepedir}/wineboot.%{wineexe}
%{_libdir}/wine/%{winepedir}/winebrowser.%{wineexe}
%{_libdir}/wine/%{winesodir}/winebrowser.exe.so
%{_libdir}/wine/%{winepedir}/wineconsole.%{wineexe}
%{_libdir}/wine/%{winepedir}/winemenubuilder.%{wineexe}
%{_libdir}/wine/%{winesodir}/winemenubuilder.exe.so
%{_libdir}/wine/%{winepedir}/winecfg.%{wineexe}
%{_libdir}/wine/%{winesodir}/winecfg.exe.so
%{_libdir}/wine/%{winepedir}/winedevice.%{wineexe}
%{_libdir}/wine/%{winepedir}/wmplayer.%{wineexe}
%{_libdir}/wine/%{winepedir}/wscript.%{wineexe}
%{_libdir}/wine/%{winepedir}/uninstaller.%{wineexe}

%{_libdir}/wine/%{winesodir}/libwine.so.1*

%{_libdir}/wine/%{winepedir}/acledit.%{winedll}
%{_libdir}/wine/%{winepedir}/aclui.%{winedll}
%{_libdir}/wine/%{winepedir}/activeds.%{winedll}
%{_libdir}/wine/%{winepedir}/activeds.%{winetlb}
%{_libdir}/wine/%{winepedir}/actxprxy.%{winedll}
%{_libdir}/wine/%{winepedir}/adsldp.%{winedll}
%{_libdir}/wine/%{winepedir}/adsldpc.%{winedll}
%{_libdir}/wine/%{winepedir}/advapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/advpack.%{winedll}
%{_libdir}/wine/%{winepedir}/amsi.%{winedll}
%{_libdir}/wine/%{winepedir}/amstream.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-identity-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-runtime-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-appmodel-runtime-l1-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-apiquery-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-appcompat-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-appinit-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-atoms-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-bem-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-com-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-comm-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-console-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-crt-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-crt-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-datetime-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-datetime-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-debug-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-debug-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-delayload-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-delayload-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-errorhandling-l1-1-3.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-fibers-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-fibers-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l1-2-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-l2-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-ansi-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-file-fromapp-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-handle-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-heap-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-interlocked-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-interlocked-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-io-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-io-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-job-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-job-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-largeinteger-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-legacy-l1-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-kernel32-private-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l1-2-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-libraryloader-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l1-2-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-obsolete-l1-3-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localization-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-localregistry-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-3.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-memory-l1-1-4.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-misc-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namedpipe-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-namespace-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-normalization-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-path-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-privateprofile-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processenvironment-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processenvironment-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-2.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processthreads-l1-1-3.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-processtopology-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-profile-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-psapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-quirks-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-realtime-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registry-l2-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-registryuserspecific-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-rtlsupport-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-rtlsupport-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shlwapi-obsolete-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-shutdown-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sidebyside-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-string-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-stringansi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-stringloader-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-l1-2-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-synch-ansi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-sysinfo-l1-2-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-systemtopology-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-threadpool-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-timezone-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-toolhelp-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-url-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-util-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-version-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-versionansi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-windowserrorreporting-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-error-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-error-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-errorprivate-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-registration-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-roparameterizediid-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-string-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-winrt-string-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-wow64-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-wow64-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-xstate-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-core-xstate-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-conio-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-convert-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-environment-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-filesystem-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-heap-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-locale-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-math-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-multibyte-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-process-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-runtime-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-stdio-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-string-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-time-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-crt-utility-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-config-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-config-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-devices-query-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-advapi32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-advapi32-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-kernel32-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-normaliz-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-ole32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shell32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shlwapi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-shlwapi-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-user32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-downlevel-version-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-dx-d3dkmt-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-classicprovider-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-consumer-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-controller-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventing-provider-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-eventlog-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-gaming-tcui-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-gdi-dpiinfo-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-joystick-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-misc-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-mme-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-mm-time-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-rectangle-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-perf-legacy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-power-base-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-power-setting-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-private-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-private-l1-1-4.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-winevent-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-rtcore-ntuser-wmpointer-l1-1-3.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-activedirectoryclient-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-audit-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-base-private-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-credentials-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-cryptoapi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-grouppolicy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsalookup-l2-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-lsapolicy-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-provider-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-sddl-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-security-systemfunctions-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-core-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-core-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-management-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-management-l2-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-private-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-winsvc-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-service-winsvc-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-obsolete-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-scaling-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-scaling-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-stream-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-stream-winrt-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shcore-thread-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shell-shellcom-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/api-ms-win-shell-shellfolders-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/apphelp.%{winedll}
%{_libdir}/wine/%{winepedir}/appwiz.%{winecpl}
%{_libdir}/wine/%{winepedir}/atl.%{winedll}
%{_libdir}/wine/%{winepedir}/atl80.%{winedll}
%{_libdir}/wine/%{winepedir}/atl90.%{winedll}
%{_libdir}/wine/%{winepedir}/atl100.%{winedll}
%{_libdir}/wine/%{winepedir}/atl110.%{winedll}
%{_libdir}/wine/%{winepedir}/atlthunk.%{winedll}
%{_libdir}/wine/%{winepedir}/atmlib.%{winedll}
%{_libdir}/wine/%{winepedir}/authz.%{winedll}
%{_libdir}/wine/%{winepedir}/avicap32.%{winedll}
%{_libdir}/wine/%{winesodir}/avicap32.dll.so
%{_libdir}/wine/%{winepedir}/avifil32.%{winedll}
%{_libdir}/wine/%{winepedir}/avrt.%{winedll}
%{_libdir}/wine/%{winesodir}/bcrypt.so
%{_libdir}/wine/%{winepedir}/bcrypt.%{winedll}
%{_libdir}/wine/%{winepedir}/bluetoothapis.%{winedll}
%{_libdir}/wine/%{winepedir}/browseui.%{winedll}
%{_libdir}/wine/%{winepedir}/bthprops.%{winecpl}
%{_libdir}/wine/%{winepedir}/cabinet.%{winedll}
%{_libdir}/wine/%{winepedir}/cards.%{winedll}
%{_libdir}/wine/%{winepedir}/cdosys.%{winedll}
%{_libdir}/wine/%{winepedir}/cfgmgr32.%{winedll}
%{_libdir}/wine/%{winepedir}/chcp.%{winecom}
%{_libdir}/wine/%{winepedir}/clock.%{wineexe}
%{_libdir}/wine/%{winepedir}/clusapi.%{winedll}
%{_libdir}/wine/%{winepedir}/combase.%{winedll}
%{_libdir}/wine/%{winepedir}/comcat.%{winedll}
%{_libdir}/wine/%{winepedir}/comctl32.%{winedll}
%{_libdir}/wine/%{winepedir}/comdlg32.%{winedll}
%{_libdir}/wine/%{winepedir}/compstui.%{winedll}
%{_libdir}/wine/%{winepedir}/comsvcs.%{winedll}
%{_libdir}/wine/%{winepedir}/concrt140.%{winedll}
%{_libdir}/wine/%{winepedir}/connect.%{winedll}
%{_libdir}/wine/%{winepedir}/credui.%{winedll}
%{_libdir}/wine/%{winesodir}/crtdll.so
%{_libdir}/wine/%{winepedir}/crtdll.%{winedll}
%{_libdir}/wine/%{winesodir}/crypt32.so
%{_libdir}/wine/%{winepedir}/crypt32.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptdlg.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptdll.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptext.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptnet.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptsp.%{winedll}
%{_libdir}/wine/%{winepedir}/cryptui.%{winedll}
%{_libdir}/wine/%{winepedir}/ctapi32.%{winedll}
%{_libdir}/wine/%{winesodir}/ctapi32.dll.so
%{_libdir}/wine/%{winepedir}/ctl3d32.%{winedll}
%{_libdir}/wine/%{winepedir}/d2d1.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/d3d10.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/d3d10_1.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/d3d10core.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-d3d10.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-d3d10_1.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-d3d10core.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/d3d11.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-d3d11.%{winedll}
%{_libdir}/wine/%{winepedir}/d3d12.%{winedll}
%{_libdir}/wine/%{winesodir}/d3d12.dll.so
%{_libdir}/wine/%{winepedir}/d3dcompiler_*.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dim.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dim700.%{winedll}
%{_libdir}/wine/%{winepedir}/d3drm.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dx9_*.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dx10_*.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dx11_42.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dx11_43.%{winedll}
%{_libdir}/wine/%{winepedir}/d3dxof.%{winedll}
%{_libdir}/wine/%{winepedir}/davclnt.%{winedll}
%{_libdir}/wine/%{winepedir}/dbgeng.%{winedll}
%{_libdir}/wine/%{winepedir}/dbghelp.%{winedll}
%{_libdir}/wine/%{winepedir}/dciman32.%{winedll}
%{_libdir}/wine/%{winepedir}/dcomp.%{winedll}
%{_libdir}/wine/%{winepedir}/ddraw.%{winedll}
%{_libdir}/wine/%{winepedir}/ddrawex.%{winedll}
%{_libdir}/wine/%{winepedir}/devenum.%{winedll}
%{_libdir}/wine/%{winepedir}/dhcpcsvc.%{winedll}
%{_libdir}/wine/%{winepedir}/dhtmled.%{wineocx}
%{_libdir}/wine/%{winepedir}/difxapi.%{winedll}
%{_libdir}/wine/%{winepedir}/dinput.%{winedll}
%{_libdir}/wine/%{winesodir}/dinput.dll.so
%{_libdir}/wine/%{winepedir}/dinput8.%{winedll}
%{_libdir}/wine/%{winesodir}/dinput8.dll.so
%{_libdir}/wine/%{winepedir}/directmanipulation.%{winedll}
%{_libdir}/wine/%{winepedir}/dispex.%{winedll}
%{_libdir}/wine/%{winepedir}/dmband.%{winedll}
%{_libdir}/wine/%{winepedir}/dmcompos.%{winedll}
%{_libdir}/wine/%{winepedir}/dmime.%{winedll}
%{_libdir}/wine/%{winepedir}/dmloader.%{winedll}
%{_libdir}/wine/%{winepedir}/dmscript.%{winedll}
%{_libdir}/wine/%{winepedir}/dmstyle.%{winedll}
%{_libdir}/wine/%{winepedir}/dmsynth.%{winedll}
%{_libdir}/wine/%{winepedir}/dmusic.%{winedll}
%{_libdir}/wine/%{winepedir}/dmusic32.%{winedll}
%{_libdir}/wine/%{winepedir}/dplay.%{winedll}
%{_libdir}/wine/%{winepedir}/dplayx.%{winedll}
%{_libdir}/wine/%{winepedir}/dpnaddr.%{winedll}
%{_libdir}/wine/%{winepedir}/dpnet.%{winedll}
%{_libdir}/wine/%{winepedir}/dpnhpast.%{winedll}
%{_libdir}/wine/%{winepedir}/dpnlobby.%{winedll}
%{_libdir}/wine/%{winepedir}/dpvoice.%{winedll}
%{_libdir}/wine/%{winepedir}/dpwsockx.%{winedll}
%{_libdir}/wine/%{winepedir}/drmclien.%{winedll}
%{_libdir}/wine/%{winepedir}/dsound.%{winedll}
%{_libdir}/wine/%{winepedir}/dsdmo.%{winedll}
%{_libdir}/wine/%{winepedir}/dsquery.%{winedll}
%{_libdir}/wine/%{winepedir}/dssenh.%{winedll}
%{_libdir}/wine/%{winepedir}/dsuiext.%{winedll}
%{_libdir}/wine/%{winepedir}/dswave.%{winedll}
%{_libdir}/wine/%{winepedir}/dwmapi.%{winedll}
%{_libdir}/wine/%{winepedir}/dwrite.%{winedll}
%{_libdir}/wine/%{winesodir}/dwrite.so
%{_libdir}/wine/%{winepedir}/dx8vb.%{winedll}
%{_libdir}/wine/%{winepedir}/dxdiagn.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/dxgi.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-dxgi.%{winedll}
%ghost %{_libdir}/wine/%{winesodir}/dxgi.dll.so
%{_libdir}/wine/%{winesodir}/wine-dxgi.dll.so
%{_libdir}/wine/%{winepedir}/dxgkrnl.%{winesys}
%{_libdir}/wine/%{winepedir}/dxgmms1.%{winesys}
%{_libdir}/wine/%{winepedir}/dxva2.%{winedll}
%{_libdir}/wine/%{winepedir}/esent.%{winedll}
%{_libdir}/wine/%{winepedir}/evr.%{winedll}
%{_libdir}/wine/%{winepedir}/explorerframe.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-authz-context-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-domainjoin-netjoin-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-dwmapi-ext-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-create-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-dc-create-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-draw-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-draw-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-font-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-font-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-gdi-render-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-kernel32-package-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-kernel32-package-current-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-dialogbox-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-draw-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-gui-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-gui-l1-3-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-keyboard-l1-3-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-5-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-message-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-message-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-misc-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-mouse-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-private-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-private-l1-3-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-rectangle-ext-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-uicontext-ext-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-window-l1-1-4.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-windowclass-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ntuser-windowclass-l1-1-1.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-oleacc-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-ras-rasapi32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-devcaps-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-object-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-gdi-rgn-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-cursor-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dc-access-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dpi-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-dpi-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-rawinput-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-syscolors-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-rtcore-ntuser-sysparams-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-security-credui-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-security-cryptui-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-comctl32-init-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-comdlg32-l1-1-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-shell-shell32-l1-2-0.%{winedll}
%{_libdir}/wine/%{winepedir}/ext-ms-win-uxtheme-themes-l1-1-0.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/ext-ms-win-appmodel-usercontext-l1-1-0.%{winedll}
%{_libdir}/wine/%{winesodir}/ext-ms-win-appmodel-usercontext-l1-1-0.dll.so
%{_libdir}/wine/%{winepedir}/ext-ms-win-xaml-pal-l1-1-0.%{winedll}
%{_libdir}/wine/%{winesodir}/ext-ms-win-xaml-pal-l1-1-0.dll.so
%endif
%{_libdir}/wine/%{winepedir}/faultrep.%{winedll}
%{_libdir}/wine/%{winepedir}/feclient.%{winedll}
%{_libdir}/wine/%{winepedir}/fltlib.%{winedll}
%{_libdir}/wine/%{winepedir}/fltmgr.%{winesys}
%{_libdir}/wine/%{winepedir}/fntcache.%{winedll}
%{_libdir}/wine/%{winepedir}/fontsub.%{winedll}
%{_libdir}/wine/%{winepedir}/fusion.%{winedll}
%{_libdir}/wine/%{winepedir}/fwpuclnt.%{winedll}
%{_libdir}/wine/%{winepedir}/gameux.%{winedll}
%{_libdir}/wine/%{winepedir}/gamingtcui.%{winedll}
%{_libdir}/wine/%{winesodir}/gdi32.so
%{_libdir}/wine/%{winepedir}/gdi32.%{winedll}
%{_libdir}/wine/%{winepedir}/gdiplus.%{winedll}
%{_libdir}/wine/%{winepedir}/glu32.%{winedll}
%{_libdir}/wine/%{winepedir}/gphoto2.%{wineds}
%{_libdir}/wine/%{winesodir}/gphoto2.ds.so
%{_libdir}/wine/%{winepedir}/gpkcsp.%{winedll}
%{_libdir}/wine/%{winepedir}/hal.%{winedll}
%{_libdir}/wine/%{winepedir}/hh.%{wineexe}
%{_libdir}/wine/%{winepedir}/hhctrl.%{wineocx}
%{_libdir}/wine/%{winepedir}/hid.%{winedll}
%{_libdir}/wine/%{winepedir}/hidclass.%{winesys}
%{_libdir}/wine/%{winepedir}/hlink.%{winedll}
%{_libdir}/wine/%{winepedir}/hnetcfg.%{winedll}
%{_libdir}/wine/%{winepedir}/http.%{winesys}
%{_libdir}/wine/%{winepedir}/httpapi.%{winedll}
%{_libdir}/wine/%{winepedir}/icacls.%{wineexe}
%{_libdir}/wine/%{winepedir}/iccvid.%{winedll}
%{_libdir}/wine/%{winepedir}/icinfo.%{wineexe}
%{_libdir}/wine/%{winepedir}/icmp.%{winedll}
%{_libdir}/wine/%{winepedir}/ieframe.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/iertutil.%{winedll}
%endif
%{_libdir}/wine/%{winepedir}/ieproxy.%{winedll}
%{_libdir}/wine/%{winepedir}/imaadp32.%{wineacm}
%{_libdir}/wine/%{winepedir}/imagehlp.%{winedll}
%{_libdir}/wine/%{winepedir}/imm32.%{winedll}
%{_libdir}/wine/%{winepedir}/inetcomm.%{winedll}
%{_libdir}/wine/%{winepedir}/inetcpl.%{winecpl}
%{_libdir}/wine/%{winepedir}/inetmib1.%{winedll}
%{_libdir}/wine/%{winepedir}/infosoft.%{winedll}
%{_libdir}/wine/%{winepedir}/initpki.%{winedll}
%{_libdir}/wine/%{winepedir}/inkobj.%{winedll}
%{_libdir}/wine/%{winepedir}/inseng.%{winedll}
%{_libdir}/wine/%{winepedir}/iphlpapi.%{winedll}
%{_libdir}/wine/%{winesodir}/iphlpapi.dll.so
%{_libdir}/wine/%{winepedir}/iprop.%{winedll}
%{_libdir}/wine/%{winepedir}/irprops.%{winecpl}
%{_libdir}/wine/%{winepedir}/itircl.%{winedll}
%{_libdir}/wine/%{winepedir}/itss.%{winedll}
%{_libdir}/wine/%{winepedir}/joy.%{winecpl}
%{_libdir}/wine/%{winepedir}/jscript.%{winedll}
%{_libdir}/wine/%{winepedir}/jsproxy.%{winedll}
%{_libdir}/wine/%{winesodir}/kerberos.so
%{_libdir}/wine/%{winepedir}/kerberos.%{winedll}
%{_libdir}/wine/%{winepedir}/kernel32.%{winedll}
%{_libdir}/wine/%{winepedir}/kernelbase.%{winedll}
%{_libdir}/wine/%{winepedir}/ksecdd.%{winesys}
%{_libdir}/wine/%{winepedir}/ksproxy.%{wineax}
%{_libdir}/wine/%{winepedir}/ksuser.%{winedll}
%{_libdir}/wine/%{winepedir}/ktmw32.%{winedll}
%if 0%{?fedora} > 24
%{_libdir}/wine/%{winepedir}/l3codeca.%{wineacm}
%{_libdir}/wine/%{winesodir}/l3codeca.acm.so
%endif
%{_libdir}/wine/%{winepedir}/loadperf.%{winedll}
%{_libdir}/wine/%{winepedir}/localspl.%{winedll}
%{_libdir}/wine/%{winepedir}/localui.%{winedll}
%{_libdir}/wine/%{winepedir}/lodctr.%{wineexe}
%{_libdir}/wine/%{winepedir}/lz32.%{winedll}
%{_libdir}/wine/%{winepedir}/mapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/mapistub.%{winedll}
%{_libdir}/wine/%{winepedir}/mciavi32.%{winedll}
%{_libdir}/wine/%{winepedir}/mcicda.%{winedll}
%{_libdir}/wine/%{winepedir}/mciqtz32.%{winedll}
%{_libdir}/wine/%{winepedir}/mciseq.%{winedll}
%{_libdir}/wine/%{winepedir}/mciwave.%{winedll}
%{_libdir}/wine/%{winepedir}/mf.%{winedll}
%{_libdir}/wine/%{winepedir}/mf3216.%{winedll}
%{_libdir}/wine/%{winepedir}/mferror.%{winedll}
%{_libdir}/wine/%{winepedir}/mfmediaengine.%{winedll}
%{_libdir}/wine/%{winepedir}/mfplat.%{winedll}
%{_libdir}/wine/%{winepedir}/mfplay.%{winedll}
%{_libdir}/wine/%{winepedir}/mfreadwrite.%{winedll}
%{_libdir}/wine/%{winepedir}/mgmtapi.%{winedll}
%{_libdir}/wine/%{winepedir}/midimap.%{winedll}
%{_libdir}/wine/%{winepedir}/mlang.%{winedll}
%{_libdir}/wine/%{winepedir}/mmcndmgr.%{winedll}
%{_libdir}/wine/%{winepedir}/mmdevapi.%{winedll}
%{_libdir}/wine/%{winepedir}/mofcomp.%{wineexe}
%{_libdir}/wine/%{winepedir}/mountmgr.%{winesys}
%{_libdir}/wine/%{winesodir}/mountmgr.sys.so
%{_libdir}/wine/%{winepedir}/mp3dmod.%{winedll}
%{_libdir}/wine/%{winesodir}/mp3dmod.dll.so
%{_libdir}/wine/%{winepedir}/mpr.%{winedll}
%{_libdir}/wine/%{winepedir}/mprapi.%{winedll}
%{_libdir}/wine/%{winepedir}/msacm32.%{winedll}
%{_libdir}/wine/%{winepedir}/msacm32.%{winedrv}
%{_libdir}/wine/%{winepedir}/msado15.%{winedll}
%{_libdir}/wine/%{winepedir}/msadp32.%{wineacm}
%{_libdir}/wine/%{winepedir}/msasn1.%{winedll}
%{_libdir}/wine/%{winepedir}/mscat32.%{winedll}
%{_libdir}/wine/%{winepedir}/mscoree.%{winedll}
%{_libdir}/wine/%{winepedir}/mscorwks.%{winedll}
%{_libdir}/wine/%{winepedir}/msctf.%{winedll}
%{_libdir}/wine/%{winepedir}/msctfp.%{winedll}
%{_libdir}/wine/%{winepedir}/msdaps.%{winedll}
%{_libdir}/wine/%{winepedir}/msdelta.%{winedll}
%{_libdir}/wine/%{winepedir}/msdmo.%{winedll}
%{_libdir}/wine/%{winepedir}/msdrm.%{winedll}
%{_libdir}/wine/%{winepedir}/msftedit.%{winedll}
%{_libdir}/wine/%{winepedir}/msg711.%{wineacm}
%{_libdir}/wine/%{winepedir}/msgsm32.%{wineacm}
%{_libdir}/wine/%{winesodir}/msgsm32.acm.so
%{_libdir}/wine/%{winepedir}/mshtml.%{winedll}
%{_libdir}/wine/%{winepedir}/mshtml.%{winetlb}
%{_libdir}/wine/%{winepedir}/msi.%{winedll}
%{_libdir}/wine/%{winepedir}/msident.%{winedll}
%{_libdir}/wine/%{winepedir}/msimtf.%{winedll}
%{_libdir}/wine/%{winepedir}/msimg32.%{winedll}
%{_libdir}/wine/%{winepedir}/msimsg.%{winedll}
%{_libdir}/wine/%{winepedir}/msinfo32.%{wineexe}
%{_libdir}/wine/%{winepedir}/msisip.%{winedll}
%{_libdir}/wine/%{winepedir}/msisys.%{wineocx}
%{_libdir}/wine/%{winepedir}/msls31.%{winedll}
%{_libdir}/wine/%{winepedir}/msnet32.%{winedll}
%{_libdir}/wine/%{winepedir}/mspatcha.%{winedll}
%{_libdir}/wine/%{winepedir}/msports.%{winedll}
%{_libdir}/wine/%{winepedir}/msscript.%{wineocx}
%{_libdir}/wine/%{winepedir}/mssign32.%{winedll}
%{_libdir}/wine/%{winepedir}/mssip32.%{winedll}
%{_libdir}/wine/%{winepedir}/msrle32.%{winedll}
%{_libdir}/wine/%{winepedir}/mstask.%{winedll}
%{_libdir}/wine/%{winepedir}/msv1_0.%{winedll}
%{_libdir}/wine/%{winesodir}/msv1_0.so
%{_libdir}/wine/%{winepedir}/msvcirt.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcm80.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcm90.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp60.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp70.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp71.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp80.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp90.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp100.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp110.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp120.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp120_app.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp140.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcp140_1.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr70.so
%{_libdir}/wine/%{winepedir}/msvcr70.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr71.so
%{_libdir}/wine/%{winepedir}/msvcr71.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr80.so
%{_libdir}/wine/%{winepedir}/msvcr80.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr90.so
%{_libdir}/wine/%{winepedir}/msvcr90.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr100.so
%{_libdir}/wine/%{winepedir}/msvcr100.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr110.so
%{_libdir}/wine/%{winepedir}/msvcr110.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcr120.so
%{_libdir}/wine/%{winepedir}/msvcr120.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcr120_app.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcrt.so
%{_libdir}/wine/%{winepedir}/msvcrt.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcrt20.%{winedll}
%{_libdir}/wine/%{winepedir}/msvcrt40.%{winedll}
%{_libdir}/wine/%{winesodir}/msvcrtd.so
%{_libdir}/wine/%{winepedir}/msvcrtd.%{winedll}
%{_libdir}/wine/%{winepedir}/msvfw32.%{winedll}
%{_libdir}/wine/%{winepedir}/msvidc32.%{winedll}
%{_libdir}/wine/%{winepedir}/mswsock.%{winedll}
%{_libdir}/wine/%{winepedir}/msxml.%{winedll}
%{_libdir}/wine/%{winepedir}/msxml2.%{winedll}
%{_libdir}/wine/%{winepedir}/msxml3.%{winedll}
%{_libdir}/wine/%{winesodir}/msxml3.dll.so
%{_libdir}/wine/%{winepedir}/msxml4.%{winedll}
%{_libdir}/wine/%{winepedir}/msxml6.%{winedll}
%{_libdir}/wine/%{winepedir}/mtxdm.%{winedll}
%{_libdir}/wine/%{winepedir}/nddeapi.%{winedll}
%{_libdir}/wine/%{winepedir}/ncrypt.%{winedll}
%{_libdir}/wine/%{winepedir}/ndis.%{winesys}
%{_libdir}/wine/%{winesodir}/netapi32.so
%{_libdir}/wine/%{winepedir}/netapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/netcfgx.%{winedll}
%{_libdir}/wine/%{winepedir}/netio.%{winesys}
%{_libdir}/wine/%{winepedir}/netprofm.%{winedll}
%{_libdir}/wine/%{winepedir}/netsh.%{wineexe}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/netutils.%{winedll}
%endif
%{_libdir}/wine/%{winepedir}/newdev.%{winedll}
%{_libdir}/wine/%{winepedir}/ninput.%{winedll}
%{_libdir}/wine/%{winepedir}/normaliz.%{winedll}
%{_libdir}/wine/%{winepedir}/npmshtml.%{winedll}
%{_libdir}/wine/%{winepedir}/npptools.%{winedll}
%{_libdir}/wine/%{winesodir}/ntdll.so
%{_libdir}/wine/%{winepedir}/ntdll.%{winedll}
%{_libdir}/wine/%{winepedir}/ntdsapi.%{winedll}
%{_libdir}/wine/%{winepedir}/ntprint.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/nvcuda.%{winedll}
%{_libdir}/wine/%{winesodir}/nvcuda.dll.so
%{_libdir}/wine/%{winepedir}/nvcuvid.%{winedll}
%{_libdir}/wine/%{winesodir}/nvcuvid.dll.so
%endif
%{_libdir}/wine/%{winepedir}/objsel.%{winedll}
%{_libdir}/wine/%{winesodir}/odbc32.so
%{_libdir}/wine/%{winepedir}/odbc32.%{winedll}
%{_libdir}/wine/%{winepedir}/odbcbcp.%{winedll}
%{_libdir}/wine/%{winepedir}/odbccp32.%{winedll}
%{_libdir}/wine/%{winepedir}/odbccu32.%{winedll}
%{_libdir}/wine/%{winepedir}/ole32.%{winedll}
%{_libdir}/wine/%{winepedir}/oleacc.%{winedll}
%{_libdir}/wine/%{winepedir}/oleaut32.%{winedll}
%{_libdir}/wine/%{winepedir}/olecli32.%{winedll}
%{_libdir}/wine/%{winepedir}/oledb32.%{winedll}
%{_libdir}/wine/%{winepedir}/oledlg.%{winedll}
%{_libdir}/wine/%{winepedir}/olepro32.%{winedll}
%{_libdir}/wine/%{winepedir}/olesvr32.%{winedll}
%{_libdir}/wine/%{winepedir}/olethk32.%{winedll}
%{_libdir}/wine/%{winepedir}/opcservices.%{winedll}
%{_libdir}/wine/%{winepedir}/packager.%{winedll}
%{_libdir}/wine/%{winepedir}/pdh.%{winedll}
%{_libdir}/wine/%{winepedir}/photometadatahandler.%{winedll}
%{_libdir}/wine/%{winepedir}/pidgen.%{winedll}
%{_libdir}/wine/%{winepedir}/powrprof.%{winedll}
%{_libdir}/wine/%{winepedir}/presentationfontcache.%{wineexe}
%{_libdir}/wine/%{winepedir}/printui.%{winedll}
%{_libdir}/wine/%{winepedir}/prntvpt.%{winedll}
%{_libdir}/wine/%{winepedir}/propsys.%{winedll}
%{_libdir}/wine/%{winepedir}/psapi.%{winedll}
%{_libdir}/wine/%{winepedir}/pstorec.%{winedll}
%{_libdir}/wine/%{winepedir}/pwrshplugin.%{winedll}
%{_libdir}/wine/%{winepedir}/qasf.%{winedll}
%{_libdir}/wine/%{winepedir}/qcap.%{winedll}
%{_libdir}/wine/%{winesodir}/qcap.so
%{_libdir}/wine/%{winepedir}/qdvd.%{winedll}
%{_libdir}/wine/%{winepedir}/qedit.%{winedll}
%{_libdir}/wine/%{winepedir}/qmgr.%{winedll}
%{_libdir}/wine/%{winepedir}/qmgrprxy.%{winedll}
%{_libdir}/wine/%{winepedir}/quartz.%{winedll}
%{_libdir}/wine/%{winepedir}/query.%{winedll}
%{_libdir}/wine/%{winepedir}/qwave.%{winedll}
%{_libdir}/wine/%{winepedir}/rasapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/rasdlg.%{winedll}
%{_libdir}/wine/%{winepedir}/regapi.%{winedll}
%{_libdir}/wine/%{winepedir}/regini.%{wineexe}
%{_libdir}/wine/%{winepedir}/resutils.%{winedll}
%{_libdir}/wine/%{winepedir}/riched20.%{winedll}
%{_libdir}/wine/%{winepedir}/riched32.%{winedll}
%{_libdir}/wine/%{winepedir}/rpcrt4.%{winedll}
%{_libdir}/wine/%{winepedir}/rsabase.%{winedll}
%{_libdir}/wine/%{winepedir}/rsaenh.%{winedll}
%{_libdir}/wine/%{winepedir}/rstrtmgr.%{winedll}
%{_libdir}/wine/%{winepedir}/rtutils.%{winedll}
%{_libdir}/wine/%{winepedir}/rtworkq.%{winedll}
%{_libdir}/wine/%{winepedir}/samlib.%{winedll}
%{_libdir}/wine/%{winepedir}/sapi.%{winedll}
%{_libdir}/wine/%{winepedir}/sas.%{winedll}
%{_libdir}/wine/%{winepedir}/sc.%{wineexe}
%{_libdir}/wine/%{winepedir}/scarddlg.%{winedll}
%{_libdir}/wine/%{winepedir}/sccbase.%{winedll}
%{_libdir}/wine/%{winepedir}/schannel.%{winedll}
%{_libdir}/wine/%{winepedir}/scrobj.%{winedll}
%{_libdir}/wine/%{winepedir}/scrrun.%{winedll}
%{_libdir}/wine/%{winepedir}/scsiport.%{winesys}
%{_libdir}/wine/%{winepedir}/sechost.%{winedll}
%{_libdir}/wine/%{winepedir}/secur32.%{winedll}
%{_libdir}/wine/%{winesodir}/secur32.so
%{_libdir}/wine/%{winepedir}/sensapi.%{winedll}
%{_libdir}/wine/%{winepedir}/serialui.%{winedll}
%{_libdir}/wine/%{winepedir}/setupapi.%{winedll}
%{_libdir}/wine/%{winepedir}/sfc_os.%{winedll}
%{_libdir}/wine/%{winepedir}/shcore.%{winedll}
%{_libdir}/wine/%{winepedir}/shdoclc.%{winedll}
%{_libdir}/wine/%{winepedir}/shdocvw.%{winedll}
%{_libdir}/wine/%{winepedir}/schedsvc.%{winedll}
%{_libdir}/wine/%{winepedir}/shell32.%{winedll}
%{_libdir}/wine/%{winesodir}/shell32.dll.so
%{_libdir}/wine/%{winepedir}/shfolder.%{winedll}
%{_libdir}/wine/%{winepedir}/shlwapi.%{winedll}
%{_libdir}/wine/%{winepedir}/shutdown.%{wineexe}
%{_libdir}/wine/%{winepedir}/slbcsp.%{winedll}
%{_libdir}/wine/%{winepedir}/slc.%{winedll}
%{_libdir}/wine/%{winepedir}/snmpapi.%{winedll}
%{_libdir}/wine/%{winepedir}/softpub.%{winedll}
%{_libdir}/wine/%{winepedir}/spoolsv.%{wineexe}
%{_libdir}/wine/%{winepedir}/srclient.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/srvcli.%{winedll}
%endif
%{_libdir}/wine/%{winepedir}/sspicli.%{winedll}
%{_libdir}/wine/%{winepedir}/stdole2.%{winetlb}
%{_libdir}/wine/%{winepedir}/stdole32.%{winetlb}
%{_libdir}/wine/%{winepedir}/sti.%{winedll}
%{_libdir}/wine/%{winepedir}/strmdll.%{winedll}
%{_libdir}/wine/%{winepedir}/subst.%{wineexe}
%{_libdir}/wine/%{winepedir}/svchost.%{wineexe}
%{_libdir}/wine/%{winepedir}/svrapi.%{winedll}
%{_libdir}/wine/%{winepedir}/sxs.%{winedll}
%{_libdir}/wine/%{winepedir}/systeminfo.%{wineexe}
%{_libdir}/wine/%{winepedir}/t2embed.%{winedll}
%{_libdir}/wine/%{winepedir}/tapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/taskkill.%{wineexe}
%{_libdir}/wine/%{winepedir}/taskschd.%{winedll}
%{_libdir}/wine/%{winepedir}/tdh.%{winedll}
%{_libdir}/wine/%{winepedir}/tdi.%{winesys}
%{_libdir}/wine/%{winepedir}/traffic.%{winedll}
%{_libdir}/wine/%{winepedir}/tzres.%{winedll}
%{_libdir}/wine/%{winesodir}/ucrtbase.so
%{_libdir}/wine/%{winepedir}/ucrtbase.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/uianimation.%{winedll}
%endif
%{_libdir}/wine/%{winepedir}/uiautomationcore.%{winedll}
%{_libdir}/wine/%{winepedir}/uiribbon.%{winedll}
%{_libdir}/wine/%{winepedir}/unicows.%{winedll}
%{_libdir}/wine/%{winepedir}/unlodctr.%{wineexe}
%{_libdir}/wine/%{winepedir}/updspapi.%{winedll}
%{_libdir}/wine/%{winepedir}/url.%{winedll}
%{_libdir}/wine/%{winepedir}/urlmon.%{winedll}
%{_libdir}/wine/%{winepedir}/usbd.%{winesys}
%{_libdir}/wine/%{winesodir}/user32.so
%{_libdir}/wine/%{winepedir}/user32.%{winedll}
%{_libdir}/wine/%{winepedir}/usp10.%{winedll}
%{_libdir}/wine/%{winepedir}/utildll.%{winedll}
%{_libdir}/wine/%{winepedir}/uxtheme.%{winedll}
%{_libdir}/wine/%{winepedir}/userenv.%{winedll}
%{_libdir}/wine/%{winepedir}/vbscript.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp90.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp100.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp110.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp120.%{winedll}
%{_libdir}/wine/%{winepedir}/vcomp140.%{winedll}
%{_libdir}/wine/%{winepedir}/vcruntime140.%{winedll}
%{_libdir}/wine/%{winepedir}/vcruntime140_1.%{winedll}
%{_libdir}/wine/%{winepedir}/vdmdbg.%{winedll}
%{_libdir}/wine/%{winepedir}/version.%{winedll}
%{_libdir}/wine/%{winepedir}/vga.%{winedll}
%{_libdir}/wine/%{winepedir}/virtdisk.%{winedll}
%{_libdir}/wine/%{winepedir}/vssapi.%{winedll}
%{_libdir}/wine/%{winepedir}/vulkan-1.%{winedll}
%{_libdir}/wine/%{winepedir}/wbemdisp.%{winedll}
%{_libdir}/wine/%{winepedir}/wbemprox.%{winedll}
%{_libdir}/wine/%{winepedir}/wdscore.%{winedll}
%{_libdir}/wine/%{winepedir}/webservices.%{winedll}
%{_libdir}/wine/%{winepedir}/websocket.%{winedll}
%{_libdir}/wine/%{winepedir}/wer.%{winedll}
%{_libdir}/wine/%{winepedir}/wevtapi.%{winedll}
%{_libdir}/wine/%{winepedir}/wevtsvc.%{winedll}
%{_libdir}/wine/%{winepedir}/wiaservc.%{winedll}
%{_libdir}/wine/%{winepedir}/wimgapi.%{winedll}
%{_libdir}/wine/%{winepedir}/win32k.%{winesys}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/windows.gaming.input.%{winedll}
%{_libdir}/wine/%{winepedir}/windows.globalization.%{winedll}
%{_libdir}/wine/%{winepedir}/windows.media.speech.%{winedll}
%endif
%{_libdir}/wine/%{winepedir}/windows.media.devices.%{winedll}
%{_libdir}/wine/%{winepedir}/windowscodecs.%{winedll}
%{_libdir}/wine/%{winesodir}/windowscodecs.so
%{_libdir}/wine/%{winepedir}/windowscodecsext.%{winedll}
%{_libdir}/wine/%{winepedir}/winebus.%{winesys}
%{_libdir}/wine/%{winesodir}/winebus.sys.so
%{_libdir}/wine/%{winesodir}/winegstreamer.so
%{_libdir}/wine/%{winepedir}/winegstreamer.%{winedll}
%{_libdir}/wine/%{winepedir}/winehid.%{winesys}
%{_libdir}/wine/%{winepedir}/winejoystick.%{winedrv}
%{_libdir}/wine/%{winesodir}/winejoystick.drv.so
%{_libdir}/wine/%{winepedir}/winemapi.%{winedll}
%{_libdir}/wine/%{winepedir}/wineusb.%{winesys}
%{_libdir}/wine/%{winesodir}/wineusb.sys.so
%{_libdir}/wine/%{winesodir}/winevulkan.so
%{_libdir}/wine/%{winepedir}/winevulkan.%{winedll}
%{_libdir}/wine/%{winepedir}/winex11.%{winedrv}
%{_libdir}/wine/%{winesodir}/winex11.drv.so
%{_libdir}/wine/%{winepedir}/wing32.%{winedll}
%{_libdir}/wine/%{winepedir}/winhttp.%{winedll}
%{_libdir}/wine/%{winepedir}/wininet.%{winedll}
%{_libdir}/wine/%{winepedir}/winmm.%{winedll}
%{_libdir}/wine/%{winepedir}/winnls32.%{winedll}
%{_libdir}/wine/%{winepedir}/winspool.%{winedrv}
%{_libdir}/wine/%{winesodir}/winspool.drv.so
%{_libdir}/wine/%{winepedir}/winsta.%{winedll}
%{_libdir}/wine/%{winepedir}/wmasf.%{winedll}
%{_libdir}/wine/%{winepedir}/wmi.%{winedll}
%{_libdir}/wine/%{winepedir}/wmic.%{wineexe}
%{_libdir}/wine/%{winepedir}/wmiutils.%{winedll}
%{_libdir}/wine/%{winepedir}/wmp.%{winedll}
%{_libdir}/wine/%{winepedir}/wmvcore.%{winedll}
%{_libdir}/wine/%{winepedir}/spoolss.%{winedll}
%{_libdir}/wine/%{winepedir}/winscard.%{winedll}
%{_libdir}/wine/%{winepedir}/wintab32.%{winedll}
%{_libdir}/wine/%{winepedir}/wintrust.%{winedll}
%{_libdir}/wine/%{winepedir}/winusb.%{winedll}
%{_libdir}/wine/%{winepedir}/wlanapi.%{winedll}
%{_libdir}/wine/%{winepedir}/wlanui.%{winedll}
%{_libdir}/wine/%{winesodir}/wmphoto.so
%{_libdir}/wine/%{winepedir}/wmphoto.%{winedll}
%{_libdir}/wine/%{winepedir}/wnaspi32.%{winedll}
%{_libdir}/wine/%{winesodir}/wnaspi32.dll.so
%if 0%{?wine_staging}
%ifarch x86_64
%{_libdir}/wine/%{winepedir}/wow64cpu.%{winedll}
%endif
%endif
%{_libdir}/wine/%{winepedir}/wpc.%{winedll}
%{_libdir}/wine/%{winepedir}/wpcap.%{winedll}
%{_libdir}/wine/%{winesodir}/wpcap.dll.so
%{_libdir}/wine/%{winepedir}/ws2_32.%{winedll}
%{_libdir}/wine/%{winesodir}/ws2_32.dll.so
%{_libdir}/wine/%{winepedir}/wsdapi.%{winedll}
%{_libdir}/wine/%{winepedir}/wshom.%{wineocx}
%{_libdir}/wine/%{winepedir}/wsnmp32.%{winedll}
%{_libdir}/wine/%{winepedir}/wsock32.%{winedll}
%{_libdir}/wine/%{winepedir}/wtsapi32.%{winedll}
%{_libdir}/wine/%{winepedir}/wuapi.%{winedll}
%{_libdir}/wine/%{winepedir}/wuaueng.%{winedll}
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/wuauserv.%{wineexe}
%endif
%{_libdir}/wine/%{winepedir}/security.%{winedll}
%{_libdir}/wine/%{winepedir}/sfc.%{winedll}
%{_libdir}/wine/%{winepedir}/wineps.%{winedrv}
%{_libdir}/wine/%{winepedir}/d3d8.%{winedll}
%{_libdir}/wine/%{winepedir}/d3d8thk.%{winedll}
%ghost %{_libdir}/wine/%{winepedir}/d3d9.%{winedll}
%{_libdir}/wine/%{winepedir}/wine-d3d9.%{winedll}
%{_libdir}/wine/%{winepedir}/opengl32.%{winedll}
%{_libdir}/wine/%{winesodir}/opengl32.dll.so
%{_libdir}/wine/%{winepedir}/wined3d.%{winedll}
%{_libdir}/wine/%{winesodir}/wined3d.dll.so
%{_libdir}/wine/%{winepedir}/dnsapi.%{winedll}
%{_libdir}/wine/%{winesodir}/dnsapi.so
%{_libdir}/wine/%{winepedir}/iexplore.%{wineexe}
%{_libdir}/wine/%{winepedir}/x3daudio1_0.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_0.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_1.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_1.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_2.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_2.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_3.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_3.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_4.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_4.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_5.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_5.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_6.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_6.dll.so
%{_libdir}/wine/%{winepedir}/x3daudio1_7.%{winedll}
%{_libdir}/wine/%{winesodir}/x3daudio1_7.dll.so
%if 0%{?wine_staging}
%{_libdir}/wine/%{winepedir}/xactengine2_0.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine2_0.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_4.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine2_4.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_7.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine2_7.dll.so
%{_libdir}/wine/%{winepedir}/xactengine2_9.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine2_9.dll.so
%endif
%{_libdir}/wine/%{winepedir}/xactengine3_0.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_0.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_1.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_1.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_2.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_2.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_3.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_3.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_4.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_4.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_5.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_5.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_6.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_6.dll.so
%{_libdir}/wine/%{winepedir}/xactengine3_7.%{winedll}
%{_libdir}/wine/%{winesodir}/xactengine3_7.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_1.%{winedll}
%{_libdir}/wine/%{winesodir}/xapofx1_1.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_2.%{winedll}
%{_libdir}/wine/%{winesodir}/xapofx1_2.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_3.%{winedll}
%{_libdir}/wine/%{winesodir}/xapofx1_3.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_4.%{winedll}
%{_libdir}/wine/%{winesodir}/xapofx1_4.dll.so
%{_libdir}/wine/%{winepedir}/xapofx1_5.%{winedll}
%{_libdir}/wine/%{winesodir}/xapofx1_5.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_0.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_0.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_1.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_1.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_2.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_2.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_3.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_3.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_4.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_4.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_5.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_5.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_6.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_6.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_7.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_7.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_8.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_8.dll.so
%{_libdir}/wine/%{winepedir}/xaudio2_9.%{winedll}
%{_libdir}/wine/%{winesodir}/xaudio2_9.dll.so
%{_libdir}/wine/%{winepedir}/xcopy.%{wineexe}
%{_libdir}/wine/%{winepedir}/xinput1_1.%{winedll}
%{_libdir}/wine/%{winepedir}/xinput1_2.%{winedll}
%{_libdir}/wine/%{winepedir}/xinput1_3.%{winedll}
%{_libdir}/wine/%{winepedir}/xinput1_4.%{winedll}
%{_libdir}/wine/%{winepedir}/xinput9_1_0.%{winedll}
%{_libdir}/wine/%{winepedir}/xmllite.%{winedll}
%{_libdir}/wine/%{winepedir}/xolehlp.%{winedll}
%{_libdir}/wine/%{winepedir}/xpsprint.%{winedll}
%{_libdir}/wine/%{winepedir}/xpssvcs.%{winedll}

%if 0%{?wine_staging}
%ifarch x86_64 aarch64
%{_libdir}/wine/%{winepedir}/nvapi64.%{winedll}
%{_libdir}/wine/%{winepedir}/nvencodeapi64.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi64.dll.so
%else
%{_libdir}/wine/%{winepedir}/nvapi.%{winedll}
%{_libdir}/wine/%{winepedir}/nvencodeapi.%{winedll}
%{_libdir}/wine/%{winesodir}/nvencodeapi.dll.so
%endif
%endif

# 16 bit and other non 64bit stuff
%ifnarch x86_64 %{arm} aarch64
%{_libdir}/wine/%{winepedir}/winevdm.exe
%{_libdir}/wine/%{winesodir}/winevdm.exe.so
%{_libdir}/wine/%{winepedir}/ifsmgr.vxd
%{_libdir}/wine/%{winepedir}/mmdevldr.vxd
%{_libdir}/wine/%{winepedir}/monodebg.vxd
%{_libdir}/wine/%{winepedir}/rundll.exe16
%{_libdir}/wine/%{winepedir}/vdhcp.vxd
%{_libdir}/wine/%{winepedir}/user.exe16
%{_libdir}/wine/%{winepedir}/vmm.vxd
%{_libdir}/wine/%{winepedir}/vnbt.vxd
%{_libdir}/wine/%{winepedir}/vnetbios.vxd
%{_libdir}/wine/%{winepedir}/vtdapi.vxd
%{_libdir}/wine/%{winepedir}/vwin32.vxd
%{_libdir}/wine/%{winepedir}/w32skrnl.dll
%{_libdir}/wine/%{winepedir}/avifile.dll16
%{_libdir}/wine/%{winepedir}/comm.drv16
%{_libdir}/wine/%{winepedir}/commdlg.dll16
%{_libdir}/wine/%{winepedir}/compobj.dll16
%{_libdir}/wine/%{winepedir}/ctl3d.dll16
%{_libdir}/wine/%{winepedir}/ctl3dv2.dll16
%{_libdir}/wine/%{winepedir}/ddeml.dll16
%{_libdir}/wine/%{winepedir}/dispdib.dll16
%{_libdir}/wine/%{winepedir}/display.drv16
%{_libdir}/wine/%{winepedir}/gdi.exe16
%{_libdir}/wine/%{winepedir}/imm.dll16
%{_libdir}/wine/%{winepedir}/krnl386.exe16
%{_libdir}/wine/%{winepedir}/keyboard.drv16
%{_libdir}/wine/%{winepedir}/lzexpand.dll16
%{_libdir}/wine/%{winepedir}/mmsystem.dll16
%{_libdir}/wine/%{winepedir}/mouse.drv16
%{_libdir}/wine/%{winepedir}/msacm.dll16
%{_libdir}/wine/%{winepedir}/msvideo.dll16
%{_libdir}/wine/%{winepedir}/ole2.dll16
%{_libdir}/wine/%{winepedir}/ole2conv.dll16
%{_libdir}/wine/%{winepedir}/ole2disp.dll16
%{_libdir}/wine/%{winepedir}/ole2nls.dll16
%{_libdir}/wine/%{winepedir}/ole2prox.dll16
%{_libdir}/wine/%{winepedir}/ole2thk.dll16
%{_libdir}/wine/%{winepedir}/olecli.dll16
%{_libdir}/wine/%{winepedir}/olesvr.dll16
%{_libdir}/wine/%{winepedir}/rasapi16.dll16
%{_libdir}/wine/%{winepedir}/setupx.dll16
%{_libdir}/wine/%{winepedir}/shell.dll16
%{_libdir}/wine/%{winepedir}/sound.drv16
%{_libdir}/wine/%{winepedir}/storage.dll16
%{_libdir}/wine/%{winepedir}/stress.dll16
%{_libdir}/wine/%{winepedir}/system.drv16
%{_libdir}/wine/%{winepedir}/toolhelp.dll16
%{_libdir}/wine/%{winepedir}/twain.dll16
%{_libdir}/wine/%{winepedir}/typelib.dll16
%{_libdir}/wine/%{winepedir}/ver.dll16
%{_libdir}/wine/%{winepedir}/w32sys.dll16
%{_libdir}/wine/%{winepedir}/win32s16.dll16
%{_libdir}/wine/%{winepedir}/win87em.dll16
%{_libdir}/wine/%{winepedir}/winaspi.dll16
%{_libdir}/wine/%{winepedir}/windebug.dll16
%{_libdir}/wine/%{winepedir}/wineps16.drv16
%{_libdir}/wine/%{winepedir}/wing.dll16
%{_libdir}/wine/%{winepedir}/winhelp.exe16
%{_libdir}/wine/%{winepedir}/winnls.dll16
%{_libdir}/wine/%{winepedir}/winoldap.mod16
%{_libdir}/wine/%{winepedir}/winsock.dll16
%{_libdir}/wine/%{winepedir}/wintab.dll16
%{_libdir}/wine/%{winepedir}/wow32.dll
%endif

%files filesystem
%doc COPYING.LIB
%dir %{_datadir}/wine
%dir %{_datadir}/wine/gecko
%dir %{_datadir}/wine/mono
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/wine.inf
%{_datadir}/wine/nls/

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
%endif
#0%%{?wine_staging}

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

%files webdings-fonts
%doc COPYING.LIB
%{_datadir}/wine/fonts/webdings.ttf

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
%{_metainfodir}/%{name}.appdata.xml
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
%{_libdir}/wine/%{winesodir}/wldap32.so
%{_libdir}/wine/%{winepedir}/wldap32.%{winedll}

# cms subpackage
%files cms
%{_libdir}/wine/%{winesodir}/mscms.so
%{_libdir}/wine/%{winepedir}/mscms.%{winedll}

# twain subpackage
%files twain
%{_libdir}/wine/%{winepedir}/twain_32.%{winedll}
%{_libdir}/wine/%{winepedir}/sane.%{wineds}
%{_libdir}/wine/%{winesodir}/sane.ds.so

# capi subpackage
%files capi
%{_libdir}/wine/%{winepedir}/capi2032.%{winedll}
%{_libdir}/wine/%{winesodir}/capi2032.dll.so

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
%{_libdir}/wine/%{winepedir}/*.a
%{_libdir}/wine/%{winesodir}/*.a
%{_libdir}/wine/%{winesodir}/*.def

%files pulseaudio
%{_libdir}/wine/%{winepedir}/winepulse.%{winedrv}
%{_libdir}/wine/%{winesodir}/winepulse.drv.so

%files alsa
%{_libdir}/wine/%{winepedir}/winealsa.%{winedrv}
%{_libdir}/wine/%{winesodir}/winealsa.drv.so

%if 0%{?fedora} >= 10 || 0%{?rhel} >= 6
%files openal
%{_libdir}/wine/%{winepedir}/openal32.%{winedll}
%{_libdir}/wine/%{winesodir}/openal32.dll.so
%endif

%if 0%{?fedora}
%files opencl
%{_libdir}/wine/%{winepedir}/opencl.%{winedll}
%{_libdir}/wine/%{winesodir}/opencl.so
%endif

%changelog
* Sat May 08 2021 Michael Cronenworth <mike@cchtml.com> 6.8-1
- version update

* Sat Apr 24 2021 Michael Cronenworth <mike@cchtml.com> 6.7-1
- version update

* Sun Apr 11 2021 Michael Cronenworth <mike@cchtml.com> 6.6-1
- version update

* Mon Mar 15 2021 Michael Cronenworth <mike@cchtml.com> 6.4-1
- version update

* Sat Feb 27 2021 Michael Cronenworth <mike@cchtml.com> 6.3-1
- version update

* Sat Feb 13 2021 Michael Cronenworth <mike@cchtml.com> 6.2-1
- version update

* Mon Feb 01 2021 Michael Cronenworth <mike@cchtml.com> 6.1-1
- version update

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Michael Cronenworth <mike@cchtml.com> 6.0-1
- version update

* Sun Jan 10 2021 Michael Cronenworth <mike@cchtml.com> 6.0-0.6rc6
- version update

* Thu Jan 07 2021 Michael Cronenworth <mike@cchtml.com> 6.0-0.5rc5
- version update

* Sat Dec 26 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.4rc4
- version update

* Sat Dec 19 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.3rc3
- version update

* Sat Dec 12 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.2rc2
- version update

* Tue Dec 08 2020 Michael Cronenworth <mike@cchtml.com> 6.0-0.1rc1
- version update

* Sat Nov 21 2020 Michael Cronenworth <mike@cchtml.com> 5.22-1
- version update

* Tue Nov 10 2020 Michael Cronenworth <mike@cchtml.com> 5.21-1
- version update

* Sat Oct 24 2020 Michael Cronenworth <mike@cchtml.com> 5.20-1
- version update

* Sat Oct 10 2020 Michael Cronenworth <mike@cchtml.com> 5.19-1
- version update

* Mon Sep 28 2020 Michael Cronenworth <mike@cchtml.com> 5.18-2
- Enable vkd3d shader support

* Mon Sep 28 2020 Michael Cronenworth <mike@cchtml.com> 5.18-1
- version update

* Tue Sep 15 2020 Michael Cronenworth <mike@cchtml.com> 5.17-1
- version update

* Tue Sep 01 2020 Michael Cronenworth <mike@cchtml.com> 5.16-1
- version update

* Sun Aug 16 2020 Michael Cronenworth <mike@cchtml.com> 5.15-1
- version update

* Mon Aug 10 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.14-2
- Recommend wine-dxvk as part of https://fedoraproject.org/wiki/Changes/DXVKwined3d

* Mon Aug 03 2020 Michael Cronenworth <mike@cchtml.com> 5.14-1
- version update

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Michael Cronenworth <mike@cchtml.com> 5.13-1
- version update

* Tue Jul 14 2020 Michael Cronenworth <mike@cchtml.com> 5.12-1
- version update

* Wed Jul 01 2020 Jeff Law <law@redhat.com> 5.10-2
- Disable LTO

* Sun Jun 07 2020 Michael Cronenworth <mike@cchtml.com> 5.10-1
- version update

* Tue Jun 02 2020 Michael Cronenworth <mike@cchtml.com> 5.9-2
- drop typelibs from 32-bit devel package
- add patch for wine bug 49208

* Fri May 29 2020 Michael Cronenworth <mike@cchtml.com> 5.9-1
- version update

* Sat May 02 2020 Michael Cronenworth <mike@cchtml.com> 5.7-2
- fix crash in wineserver affecting many apps and games (RHBZ#1829956)

* Sun Apr 26 2020 Michael Cronenworth <mike@cchtml.com> 5.7-1
- version update

* Sat Apr 11 2020 Michael Cronenworth <mike@cchtml.com> 5.6-1
- version update

* Sun Mar 29 2020 Michael Cronenworth <mike@cchtml.com> 5.5-1
- version update

* Mon Mar 16 2020 Michael Cronenworth <mike@cchtml.com> 5.4-1
- version update

* Mon Mar 02 2020 Michael Cronenworth <mike@cchtml.com> 5.3-1
- version update

* Tue Feb 18 2020 Michael Cronenworth <mike@cchtml.com> 5.2-1
- version update

* Mon Feb 03 2020 Michael Cronenworth <mike@cchtml.com> 5.1-1
- version update

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Michael Cronenworth <mike@cchtml.com> 5.0-1
- version update

* Mon Jan 13 2020 Michael Cronenworth <mike@cchtml.com> 5.0-0.rc5.0
- version update

* Mon Jan 06 2020 Michael Cronenworth <mike@cchtml.com> 5.0-0.rc4.0
- version update

* Mon Dec 30 2019 Michael Cronenworth <mike@cchtml.com> 5.0-0.rc3.0
- version update

* Sat Nov 30 2019 Michael Cronenworth <mike@cchtml.com> 4.21-1
- version update

* Sat Nov 16 2019 Michael Cronenworth <mike@cchtml.com> 4.20-1
- version and wine-mono update

* Sat Nov 02 2019 Michael Cronenworth <mike@cchtml.com> 4.19-1
- version update

* Mon Oct 21 2019 Michael Cronenworth <mike@cchtml.com> 4.18-1
- version update

* Sun Sep 29 2019 Michael Cronenworth <mike@cchtml.com> 4.17-2
- sync wine-mono version

* Sat Sep 28 2019 Michael Cronenworth <mike@cchtml.com> 4.17-1
- version update

* Thu Sep 26 2019 Michael Cronenworth <mike@cchtml.com> 4.16-2
- Drop isdn4k-utils BR (RHBZ#1756118)

* Sat Sep 14 2019 Michael Cronenworth <mike@cchtml.com> 4.16-1
- version update

* Sun Sep 01 2019 Michael Cronenworth <mike@cchtml.com> 4.15-1
- version update

* Mon Aug 19 2019 Michael Cronenworth <mike@cchtml.com> 4.14-2
- sync wine-mono version

* Mon Aug 19 2019 Michael Cronenworth <mike@cchtml.com> 4.14-1
- version update

* Sun Aug 11 2019 Michael Cronenworth <mike@cchtml.com> 4.13-5
- remove correct dlls on upgrade

* Thu Aug 08 2019 Michael Cronenworth <mike@cchtml.com> 4.13-4
- support upgrades in new alternatives

* Wed Aug 07 2019 Michael Cronenworth <mike@cchtml.com> 4.13-3
- fix slave alternatives for d3d dlls

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

