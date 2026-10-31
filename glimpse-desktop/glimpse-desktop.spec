# Workspace profile.release sets strip = true
%global debug_package %{nil}

%global binaries glimpsectl glimpse-panel glimpse-lock glimpse-wallpaper glimpse-sunset glimpse-notifications glimpse-agents glimpse-weather glimpse-calendar glimpse-idle glimpse-lens glimpse-shot glimpse-settings-daemon glimpse-compositor-niri glimpse-compositor-hyprland

%global upstream glimpse

Name:    glimpse-desktop
Version: 0.16.1
Release: 1%{?dist}
Summary: Desktop shell suite for Wayland compositors (niri, Hyprland)
License: BSD-3-Clause
URL:     https://github.com/alex-oleshkevich/glimpse
Source0: %{url}/archive/v%{version}/%{upstream}-%{version}.tar.gz

ExclusiveArch: aarch64 x86_64

BuildRequires: rust >= 1.95
BuildRequires: cargo
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: clang-devel
BuildRequires: cmake
BuildRequires: perl-interpreter
BuildRequires: blueprint-compiler
BuildRequires: gettext
BuildRequires: pkgconfig(gtk4) >= 4.22
BuildRequires: pkgconfig(libadwaita-1) >= 1.9
BuildRequires: pkgconfig(gtk4-layer-shell-0) >= 1.2
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(zlib)
BuildRequires: pam-devel
BuildRequires: systemd-rpm-macros

Requires: gtk4%{?_isa} >= 4.22
Requires: libadwaita%{?_isa} >= 1.9
Requires: gtk4-layer-shell%{?_isa} >= 1.2
Requires: geoclue2
Requires: ddcutil
Requires: pam

Recommends: upower
Recommends: power-profiles-daemon
Recommends: NetworkManager
Recommends: bluez
Recommends: udisks2
Recommends: xdg-desktop-portal
Recommends: wl-clipboard
Suggests:   cups
Suggests:   kdeconnectd

%description
glimpse is a desktop shell for Wayland compositors built with GTK4 and
libadwaita: panel with applets, wallpaper, lock screen, notifications,
idle manager, night light, polkit agent, screenshots and clipboard history.

This build does not install the niri/Hyprland portal overrides into
/etc/xdg-desktop-portal; reference copies live in %{_datadir}/glimpse/portals.

%prep
%autosetup -n %{upstream}-%{version}

%build
export CARGO_HOME=%{_builddir}/.cargo
export PREFIX=%{_prefix}
export GETTEXT_SYSTEM=1
args=()
for b in %{binaries}; do args+=(--bin "$b"); done
cargo build --release --locked "${args[@]}"
GLIMPSE_LANGUAGES="$(tr '\n' ' ' < po/LINGUAS)" scripts/i18n-build.sh

%install
DESTDIR=%{buildroot} PREFIX=%{_prefix} GLIMPSE_BINARIES="%{binaries}" scripts/install.sh

# Fedora PAM stack (install.sh picks the generic file on the build host)
install -Dpm0644 data/pam.d/fedora/glimpse-lock %{buildroot}%{_sysconfdir}/pam.d/glimpse-lock

# Compositor portal overrides would shadow niri's own portals.conf system-wide
rm -f %{buildroot}%{_sysconfdir}/xdg-desktop-portal/niri-portals.conf
rm -f %{buildroot}%{_sysconfdir}/xdg-desktop-portal/hyprland-portals.conf

%find_lang %{upstream}

%files -f %{upstream}.lang
%license LICENSE
%{_bindir}/glimpse*
%{_userunitdir}/glimpse-*.service
%{_userunitdir}/glimpse-session.target
%{_datadir}/dbus-1/services/me.aresa.Glimpse.*.service
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%{_datadir}/dbus-1/services/org.freedesktop.ScreenSaver.service
%{_datadir}/applications/me.aresa.Glimpse.*.desktop
%{_metainfodir}/me.aresa.Glimpse.Shot.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/me.aresa.Glimpse*.svg
%{_datadir}/icons/hicolor/symbolic/apps/me.aresa.Glimpse*.svg
%{_datadir}/xdg-desktop-portal/portals/*.portal
%{_datadir}/glimpse/
%dir %{_sysconfdir}/xdg-desktop-portal
%config(noreplace) %{_sysconfdir}/xdg-desktop-portal/glimpse-portals.conf
%config(noreplace) %{_sysconfdir}/pam.d/glimpse-lock
%config(noreplace) %{_sysconfdir}/geoclue/conf.d/glimpse.conf

%changelog
* Fri Oct 30 2026 Eugene <e.rusalev@gmail.com> - 0.16.1-1
- Initial COPR packaging
- Package renamed to glimpse-desktop (Fedora already ships an unrelated glimpse)
