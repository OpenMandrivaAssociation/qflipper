%undefine _debugsource_packages

%global commit 8e43ad60f0a53fe771880aab4d225a57acc2cbbc
# git log -1 --pretty=format:%ct
%global timestamp 1684846555
%global nanopb_commit 13666952914f3cf43a70c6b9738a7dc0dd06a6dc

%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	Desktop application for updating Flipper Zero firmware via PC
Name:		qflipper
Version:	1.3.1
Release:	1
# qFlipper proper is GPLv3, the bundled nanopb library is zlib
License:	GPLv3 and zlib
URL:		https://flipperzero.one/update
Source0:	https://github.com/flipperdevices/qFlipper/archive/%{version}/qFlipper-%{version}.tar.gz
Source1:	https://github.com/nanopb/nanopb/archive/%{nanopb_commit}/nanopb-%{nanopb_commit}.tar.gz
Source2:	42-flipperzero.rules
Source3:	one.flipperzero.qflipper.metainfo.xml

BuildRequires:	pkgconfig(appstream)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(Qt5QuickControls2)
BuildRequires:	pkgconfig(Qt5SerialPort)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-qtbase-devel

#Requires:	systemd-udev

# nanopb needs to be compiled in, and needs to match the one used in the
# firmware on the device side
#Provides:	bundled(nanopb) = 0.4.5

%description
Desktop application for updating Flipper Zero firmware via PC.

  *  Update Flipper's firmware and supplemental data with a press of one button
  *  Repair a broken firmware installation
  *  Stream Flipper's display and control it remotely
  *  Install firmware from a .dfu file
  *  Backup and restore settings, progress and pairing data
  *  Automatic self-update feature
  *  Command line interface

%files
%license LICENSE 3rdparty/nanopb/LICENSE.txt
%doc README.md screenshot.png
%{_bindir}/*
%{_libdir}/qFlipper
%{_datadir}/applications/qFlipper.desktop
%{_datadir}/icons/hicolor/512x512/apps/qFlipper.png
%{_metainfodir}/one.flipperzero.qflipper.metainfo.xml
%{_udevrulesdir}/42-flipperzero.rules

#---------------------------------------------------------------------------

%prep
%autosetup -n qFlipper-%{version} -b1

# Use the correct nanopb snapshot
rmdir 3rdparty/nanopb
ln -s ../../nanopb-%{nanopb_commit} 3rdparty/nanopb

# set the version
sed -i qflipper_common.pri \
	-e 's/$$GIT_VERSION/%{version}/' \
	-e 's/$$GIT_COMMIT/%{shortcommit}/' \
	-e 's/$$GIT_TIMESTAMP/%{timestamp}/'

# fix the plugins library path
sed -e 's:/lib/:/%{_lib}/:' \
	-i backend/applicationbackend.cpp plugins/flipperproto0/flipperproto0.pro

%build
%qmake_qt5 \
	PREFIX=%{buildroot}%{_prefix} \
	CONFIG+=qtquickcompiler \
	DEFINES+=DISABLE_APPLICATION_UPDATES
%make_build

%install
%make_install

# udev rules
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} %SOURCE2

# appdata file
install -Dpm0644 -t %{buildroot}%{_metainfodir} %SOURCE3

