# Keep libraries private
%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{_libdir}/ardour3
%define __noautoreq 'libardour\\.so(.*)|libardourcp\\.so(.*)|libvamphost\\.so(.*)|libtaglib\\.so(.*)|libgtkmm2ext\\.so(.*)|librubberband\\.so(.*)|libpbd\\.so(.*)|libqmdsp\\.so(.*)|libaudiographer\\.so(.*)|libsmf\\.so(.*)|libevoral\\.so(.*)|libtimecode\\.so(.*)|libltc\\.so(.*)|libvampplugin\\.so(.*)|libmidipp\\.so(.*)'
%endif

%define oname	ardour

Summary:	Professional multi-track audio recording application
Name:		ardour3
Version:	3.2
Release:	2
Group:		Sound
License:	GPLv2+
Url:		http://ardour.org/
Source0:	%{oname}-%{version}.tar.bz2
Source1:	ardour3.desktop
# MUST be removed when version 3.3+ is released
Source2:	ardour3-3.2-ru.po
BuildRequires:	boost-devel
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	graphviz
BuildRequires:	shared-mime-info
BuildRequires:	xdg-utils
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(aubio) >= 0.3.2
BuildRequires:	pkgconfig(cppunit) >= 1.12.0
BuildRequires:	pkgconfig(cwiid)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flac) >= 1.2.1
BuildRequires:	pkgconfig(glib-2.0) >= 2.2
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gtkmm-2.4)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libart-2.0)
BuildRequires:	pkgconfig(libcurl) >= 7.0.0
BuildRequires:	pkgconfig(libgnomecanvas-2.0) >= 2.30
BuildRequires:	pkgconfig(libgnomecanvasmm-2.6) >= 2.16
BuildRequires:	pkgconfig(liblo) >= 0.24
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(lilv-0) >= 0.14
BuildRequires:	pkgconfig(lrdf) >= 0.4.0
BuildRequires:	pkgconfig(ltc) >= 1.1.0
BuildRequires:	pkgconfig(lv2) >= 1.0.15
BuildRequires:	pkgconfig(ogg) >= 1.1.2
BuildRequires:	pkgconfig(raptor2)
BuildRequires:	pkgconfig(redland)
BuildRequires:	pkgconfig(rubberband)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(serd-0) >= 0.14.0
BuildRequires:	pkgconfig(sndfile) >= 1.0.18
BuildRequires:	pkgconfig(sord-0) >= 0.8.0
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(sratom-0) >= 0.4.0
BuildRequires:	pkgconfig(suil-0) >= 0.6.0
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(vamp-sdk)

Requires:	jackit
Requires:	gtk-engines2

# For video import
Requires:	harvid
Requires:	xjadeo

%description
Ardour3 is a digital audio workstation. You can use it to record, edit and mix
multi-track audio. You can produce your own CDs, mix video sound tracks, or
just experiment with new ideas about music and sound.

Ardour3 capabilities include: multi channel recording, non-destructive editing
with unlimited undo/redo, full automation support, a powerful mixer, unlimited
tracks/busses/plugins, time-code synchronization, and hardware control from
surfaces like the Mackie Control Universal.

You must have jackd running and an ALSA sound driver to use Ardour3. If you are
new to jackd, try qjackctl.

See the online user manual at http://en.flossmanuals.net/ardour/index/

%prep
%setup -q -n %{oname}-%{version}
cp %{SOURCE2} gtk2_ardour/po/ru.po

%build
./waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --configdir=%{_sysconfdir} \
    --program-name=Ardour3 \
    --nls \
    --docs

./waf build \
    --nls \
    --docs

./waf i18n_mo

%install
./waf install --destdir=%{buildroot}

install -d -m 0755 %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/applications/

install -d -m 0755 %{buildroot}%{_iconsdir}
cp -f %{buildroot}%{_datadir}/%{name}/icons/application-x-ardour_48px.png %{buildroot}%{_iconsdir}/ardour3.png

%find_lang %{name} gtk2_ardour3 gtkmm2ext3 %{name}.lang

%files -f %{name}.lang
%doc README
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/sanityCheck
%{_libdir}/%{name}/ardour-%{version}
%{_libdir}/%{name}/*.so.*
%{_libdir}/%{name}/panners/*.so
%{_libdir}/%{name}/panners/*.so.*
%{_libdir}/%{name}/surfaces/*.so
%{_libdir}/%{name}/surfaces/*.so.*
%{_libdir}/%{name}/engines/*.so
%{_libdir}/%{name}/vamp/*.so
%{_libdir}/%{name}/vamp/*.so.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.ttf
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/*.png
%dir %{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/pixmaps/*.xpm
%{_datadir}/%{name}/export/*
%{_datadir}/%{name}/mcp/*
%{_datadir}/%{name}/patchfiles/*
%{_datadir}/%{name}/midi_maps/*
%attr(0644, root, root) %{_datadir}/applications/ardour3.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}_ui_default.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}_ui_light.rc
%config(noreplace) %{_sysconfdir}/%{name}/%{name}_ui_dark.rc
%config(noreplace) %{_sysconfdir}/%{name}/ardour.menus
%config(noreplace) %{_sysconfdir}/%{name}/ardour_system.rc
%config(noreplace) %{_sysconfdir}/%{name}/step_editing.bindings
%config(noreplace) %{_sysconfdir}/%{name}/mnemonic-us.bindings
%config(noreplace) %{_sysconfdir}/%{name}/mixer.bindings
%dir %{_sysconfdir}/%{name}/export
%config(noreplace) %{_sysconfdir}/%{name}/export/CD.format
%{_iconsdir}/ardour3.png
