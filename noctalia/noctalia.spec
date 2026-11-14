%global appid dev.noctalia.Noctalia

Name:    noctalia
Version: 5.5.0
Release: 901%{?dist}.barbg1
Summary: A sleek, customizable desktop shell crafted for Wayland
# noctalia, fzy, luau: MIT; material-color-utilities: Apache-2.0; wuffs: Apache-2.0 OR MIT
License: MIT AND Apache-2.0 AND (Apache-2.0 OR MIT)
URL:     https://github.com/noctalia-dev/noctalia
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Configurable bar background: [bar.<n>] background = "<role>|#hex"
Patch0:  0001-bar-configurable-background-color.patch

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
Requires: sound-theme-freedesktop
Recommends: upower
Recommends: power-profiles-daemon
Recommends: ddcutil
# Secret Service backend for libsecret
Recommends: (oo7-daemon or gnome-keyring or kf6-kwallet)
# dlopen()ed for HEIF/AVIF decoding
Recommends: libheif.so.1()(%{__isa_bits}bit)

Provides: bundled(fzy) = 1.1
Provides: bundled(luau) = 0.742
Provides: bundled(material_color_utilities)
Provides: bundled(wuffs) = 0.4.0~alpha.9

%description
Noctalia is a Wayland desktop shell: bars, dock, launcher, notifications,
lock screen, wallpaper and settings, rendered with OpenGL ES.

This build carries a local patch: a configurable bar background color
([bar.<n>] background, also per monitor).

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

noctalia=%{buildroot}%{_bindir}/noctalia
install -d %{buildroot}%{bash_completions_dir} %{buildroot}%{fish_completions_dir} %{buildroot}%{zsh_completions_dir}
$noctalia completions bash > %{buildroot}%{bash_completions_dir}/noctalia
$noctalia completions fish > %{buildroot}%{fish_completions_dir}/noctalia.fish
$noctalia completions zsh  > %{buildroot}%{zsh_completions_dir}/_noctalia

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.Annotator.desktop

%files
%license LICENSE
%license third_party/fzy/LICENSE
%license third_party/luau/LICENSE.txt third_party/luau/lua_LICENSE.txt
%license third_party/material_color_utilities/LICENSE
%license lib/third_party/wuffs/LICENSE-APACHE lib/third_party/wuffs/LICENSE-MIT
%license lib/assets/fonts/tabler-icons-license.txt
%doc README.md
%{_bindir}/noctalia
%{_datadir}/noctalia/
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/applications/%{appid}.Annotator.desktop
%{_datadir}/icons/hicolor/scalable/apps/noctalia.svg
%{bash_completions_dir}/noctalia
%{fish_completions_dir}/noctalia.fish
%{zsh_completions_dir}/_noctalia

%changelog
* Sat Nov 14 2026 Eugene <e.rusalev@gmail.com> - 5.5.0-901.barbg1
- Bump release to 9xx so the COPR build outranks Fedora's noctalia
- Ship bash/fish/zsh completions
- Require sound-theme-freedesktop, recommend a Secret Service backend,
  recommend libheif by soname
- Add luau lua and tabler icons licenses

* Sat Nov 14 2026 Eugene <e.rusalev@gmail.com> - 5.5.0-1.barbg1
- Update to 5.5.0
- Rebase bar background patch (schema moved to config_schema_bar.cpp)
- Drop tray colorization patch: upstream [widget.tray] colorize_icons

* Fri Nov 06 2026 Eugene <e.rusalev@gmail.com> - 5.4.1-2.barbg1
- Add optional tray icon colorization (local patch)

* Sun Nov 01 2026 Eugene <e.rusalev@gmail.com> - 5.4.1-1.barbg1
- Update to 5.4.1
- Add configurable bar background color (local patch)
