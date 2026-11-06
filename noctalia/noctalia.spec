%global appid dev.noctalia.Noctalia

Name:    noctalia
Version: 5.4.1
Release: 2%{?dist}.barbg1
Summary: A sleek, customizable desktop shell crafted for Wayland
# noctalia, fzy, luau: MIT; material-color-utilities: Apache-2.0; wuffs: Apache-2.0 OR MIT
License: MIT AND Apache-2.0 AND (Apache-2.0 OR MIT)
URL:     https://github.com/noctalia-dev/noctalia
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Configurable bar background: [bar.<n>] background = "<role>|#hex"
Patch0:  0001-bar-configurable-background-color.patch
# Tray icon colorization: [widget.tray] colorize = true
Patch1:  0002-tray-optional-icon-colorization.patch

ExclusiveArch: aarch64 x86_64

BuildRequires: meson >= 1.1
BuildRequires: gcc
BuildRequires: gcc-c++ >= 13
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(sdbus-c++)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(cairo-ft)
BuildRequires: pkgconfig(pango) >= 1.50
BuildRequires: pkgconfig(pangocairo)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(libsecret-1) >= 0.20
BuildRequires: pkgconfig(libsodium) >= 1.0.18
BuildRequires: pkgconfig(polkit-agent-1)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(wireplumber-0.5)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libqalculate)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(md4c)
BuildRequires: pkgconfig(nlohmann_json)
BuildRequires: pkgconfig(tomlplusplus)
BuildRequires: pkgconfig(libical)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libwebpdemux)
BuildRequires: pkgconfig(libjxl)
BuildRequires: pkgconfig(libjxl_threads)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pam-devel
BuildRequires: stb_image_resize2-devel
BuildRequires: stb_image_write-devel

Requires: hicolor-icon-theme
Requires: pipewire
Requires: wireplumber
Requires: git-core
Recommends: upower
Recommends: power-profiles-daemon
Recommends: ddcutil
Recommends: sound-theme-freedesktop
Recommends: libheif

Provides: bundled(fzy) = 1.1
Provides: bundled(luau) = 0.742
Provides: bundled(material_color_utilities)
Provides: bundled(wuffs) = 0.4.0~alpha.9

%description
Noctalia is a Wayland desktop shell: bars, dock, launcher, notifications,
lock screen, wallpaper and settings, rendered with OpenGL ES.

This build carries local patches: a configurable bar background color
([bar.<n>] background, also per monitor) and optional tray icon
colorization ([widget.tray] colorize).

%prep
%autosetup -p1

%build
%meson \
    -Dtests=disabled \
    -Djemalloc=enabled \
    -Dnative_optimizations=false
%meson_build

%install
%meson_install

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.Annotator.desktop

%files
%license LICENSE
%license third_party/fzy/LICENSE
%license third_party/luau/LICENSE.txt
%license third_party/material_color_utilities/LICENSE
%license third_party/wuffs/LICENSE-APACHE third_party/wuffs/LICENSE-MIT
%doc README.md
%{_bindir}/noctalia
%{_datadir}/noctalia/
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/applications/%{appid}.Annotator.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg

%changelog
* Fri Nov 06 2026 Eugene <e.rusalev@gmail.com> - 5.4.1-2.barbg1
- Add optional tray icon colorization (local patch)

* Sun Nov 01 2026 Eugene <e.rusalev@gmail.com> - 5.4.1-1.barbg1
- Update to 5.4.1
- Add configurable bar background color (local patch)
