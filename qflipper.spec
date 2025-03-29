%undefine _debugsource_packages

# git log -1 --pretty=format:%ct
%global timestamp 1686221902
%global commit 7b0839e178b98ba77f732fc679141a82a90c67dc
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	Desktop application for updating Flipper Zero firmware via PC
Name:		qflipper
Version:	1.3.3
Release:	3
License:	GPLv3
Group:		Development/Other
URL:		https://flipperzero.one/update
Source0:	https://github.com/flipperdevices/qFlipper/archive/%{version}/qFlipper-%{version}.tar.gz
Source2:	42-flipperzero.rules
Source3:	one.flipperzero.qflipper.metainfo.xml
#Patch0:		qflipper-1.3.3-unbundle_nanopb.patch

BuildRequires:	cmake ninja
BuildRequires:	cmake(FastFloat)
BuildRequires:	cmake(nanopb)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Core5Compat)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6SerialPort)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6UiPlugin)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	pkgconfig(appstream)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	qt6-qttools-linguist-tools

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
%license LICENSE
%doc README.md screenshot.png
%{_bindir}/*
%{_libdir}/qFlipper
%{_datadir}/applications/qFlipper.desktop
%{_datadir}/icons/hicolor/512x512/apps/qFlipper.png
%{_metainfodir}/one.flipperzero.qflipper.metainfo.xml
%{_udevrulesdir}/42-flipperzero.rules

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n qFlipper-%{version}

# Use the system library
#rmdir 3rdparty/nanopb

# set the version
sed -i qflipper_common.pri \
	-e 's/$$GIT_VERSION/%{version}/' \
	-e 's/$$GIT_COMMIT/%{shortcommit}/' \
	-e 's/$$GIT_TIMESTAMP/%{timestamp}/'

# fix the plugins library path
sed -e 's:/lib/:/%{_lib}/:' \
	-i backend/applicationbackend.cpp plugins/flipperproto0/flipperproto0.pro

%build
%set_build_flags
mkdir -p build && cd build
qmake-qt6 \
	PREFIX=%{buildroot}%{_prefix} \
	CONFIG+="qtquickcompiler" \
	DEFINES+=DISABLE_APPLICATION_UPDATES \
	"../qFlipper.pro"
%make_build

%install
%make_install -C build

# udev rules
install -Dpm0644 -t %{buildroot}%{_udevrulesdir} %SOURCE2

# appdata file
install -Dpm0644 -t %{buildroot}%{_metainfodir} %SOURCE3
 
