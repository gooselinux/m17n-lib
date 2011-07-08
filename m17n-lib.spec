# set to 1 to build with GUI and OpenType Font support
%define with_gui 0
# set to 1 to build examples (including anthy support)
%define with_examples 0

Name:    m17n-lib
Version:  1.5.5
Release:  2%{?dist}
Summary:  Multilingual text library

Group:    System Environment/Libraries
License:  LGPLv2+
URL:    http://www.m17n.org/m17n-lib/index.html
Source0:  http://www.m17n.org/m17n-lib-download/%{name}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  m17n-db >= 1.4.0
%if %{with_gui}
BuildRequires:  libxml2-devel, xorg-x11-devel
BuildRequires:  freetype-devel >= 2.0, fribidi-devel, gd-devel >= 2.0
BuildRequires:  libotf-devel >= %{libotf_version}
%else
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
%endif
%if %{with_examples}
BuildRequires:  anthy-devel
%endif
Requires:  m17n-db >= 1.4.0
Patch2:    m17n-lib-nobuild-examples.patch

%description
m17n-lib is a multilingual text library used primarily to allow
the input of many languages with the input table maps from m17n-db.


%package  devel
Summary:  m17n-lib development files
Group:    Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
Development files for %{name}.


%prep
%setup -q

%if ! %{with_examples}
%patch2 -p1 -b .examples
%endif
# patch2 touches Makefile.am
autoreconf

%build
%configure --disable-static \
%if ! %{with_gui}
  --with-gui=no
%else
  %{nil}
%endif
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

# remove unneeded files
rm $RPM_BUILD_ROOT%{_bindir}/m17n-config
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%doc ChangeLog README
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*


%changelog
* Thu Feb 25 2010 Parag <pnemade AT redhat.com> - 1.5.5-2
- Resolves:rh#568302 - Fix license tag to LPGLv2+

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.5.5-1.1
- Rebuilt for RHEL 6

* Mon Aug 17 2009 Parag Nemade <pnemade@redhat.com> -1.5.5-1
- update to new upstream release 1.5.5

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Parag Nemade <pnemade@redhat.com> -1.5.4-1
- Update to new upstream release 1.5.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 21 2008 Parag Nemade <pnemade@redhat.com> -1.5.3-1.fc10
- Update to new upstream release 1.5.3

* Thu Jul 03 2008 Parag Nemade <pnemade@redhat.com> -1.5.2-1
- Update to new upstream release 1.5.2

* Thu Feb 07 2008 Parag Nemade <pnemade@redhat.com> -1.5.1-1.fc9
- Update to new upstream release 1.5.1

* Fri Dec 28 2007 Parag Nemade <pnemade@redhat.com> -1.5.0-1.fc9
- Update to new upstream release 1.5.0
- Added missing internal-flt.h file as Source1

* Wed Aug 22 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-2
- rebuild against new rpm package
- update license tag

* Thu Jul 19 2007 Jens Petersen <petersen@redhat.com>
- buildrequire and require m17n-db >= 1.4.0

* Thu Jul 19 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-1
- Updated to new upstream release 1.4.0

* Wed Jan 10 2007 Mayank Jain <majain@redhat.com> - 1.3.4-1.1.fc7
- rebuild for m17n-lib-1.3.4 version
- Updated m17n-lib-nobuild-examples.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.3-1.1.fc6
- rebuild

* Wed Jul 12 2006 Mayank Jain <majain@redhat.com> - 1.3.3-1.fc6
- Updated spec file for changes mentioned in RH bug 193524, comment 4
- Thanks to Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- update to 1.3.3 minor bugfix release

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.2-1.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- update to 1.3.2 bugfix release
  - m17n-lib-no-gui-headers.patch is now upstream

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.1-1
- update to 1.3.1 release
  - rename use_otf and use_anthy macros to with_gui and with_examples
  - build --with-gui=no and replace m17n-lib-1.2.0-core-libs-only.patch
    with m17n-lib-no-gui-headers.patch and m17n-lib-nobuild-examples.patch

* Fri Dec 16 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-2
- import to Fedora Core
- buildrequire autoconf

* Thu Nov 10 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-1
- do not build static lib and .la files (Warren Togami)

* Wed Oct  5 2005 Jens Petersen <petersen@redhat.com>
- initial packaging for Fedora Extras

* Sat Jan 15 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp>
- modify spec for fedora
