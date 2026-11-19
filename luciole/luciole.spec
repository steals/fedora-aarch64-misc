%global commit 0b37f2cc760c241ce2cf78dbdc4744f18a5b66b7
%global shortcommit %{sub %{commit} 1 7}
%global appid dev.noctalia.luciole

Name:    luciole
Version: 0.1.0~20261119git%{shortcommit}
Release: 1%{?dist}
Summary: Native Wayland file manager with tabs, split view, and previews
License: MIT
URL:     https://github.com/noctalia-dev/luciole
Source0: %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

ExclusiveArch: aarch64 x86_64

BuildRequires: meson >= 1.1
BuildRequires: gcc
BuildRequires: gcc-c++ >= 15
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(wayland-protocols) >= 1.49
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(gio-2.0) >= 2.76
BuildRequires: pkgconfig(gio-unix-2.0) >= 2.76
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libcurl) >= 7.85
BuildRequires: pkgconfig(libxml-2.0) >= 2.9
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= 2.42
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(cairo-ft)
BuildRequires: pkgconfig(pango) >= 1.50
BuildRequires: pkgconfig(pangocairo)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libarchive)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libacl)
BuildRequires: pkgconfig(tomlplusplus) >= 3.4
BuildRequires: pkgconfig(nlohmann_json)
BuildRequires: stb_image_resize2-devel

Requires: gvfs
Requires: gsettings-desktop-schemas
Requires: shared-mime-info
Requires: hicolor-icon-theme
Recommends: adwaita-icon-theme
Recommends: dconf
Recommends: glib-networking
Recommends: gvfs-smb
Recommends: /usr/bin/ffmpeg
Recommends: /usr/bin/ffprobe
Recommends: ffmpegthumbnailer
Recommends: poppler-utils
Recommends: 7zip

%description
Luciole is a native Wayland file manager with tabbed browsing, split view,
Miller columns, file previews, and archive support. It also ships an
xdg-desktop-portal FileChooser backend.

%prep
%autosetup -n %{name}-%{commit}

%build
%meson \
    -Dtests=disabled \
    -Dnative_optimizations=false \
    -Dbuild_revision=%{shortcommit} \
    -Dwerror=false
%meson_build

%install
%meson_install
rm %{buildroot}%{_datadir}/licenses/%{name}/LICENSE

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
%{buildroot}%{_bindir}/luciole --version | grep -F '%{shortcommit}'

%files
%license LICENSE
%doc README.md
%{_bindir}/luciole
%{_datadir}/luciole/
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/dbus-1/services/%{appid}.FileManager1.service
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.desktop.luciole.service
%dir %{_datadir}/xdg-desktop-portal
%dir %{_datadir}/xdg-desktop-portal/portals
%{_datadir}/xdg-desktop-portal/portals/luciole.portal
%{bash_completions_dir}/luciole
%{zsh_completions_dir}/_luciole
%{fish_completions_dir}/luciole.fish

%changelog
* Thu Nov 19 2026 Eugene <e.rusalev@gmail.com> - 0.1.0~20261119git0b37f2c-1
- Initial package from upstream Git snapshot.
