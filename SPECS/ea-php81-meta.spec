# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel

%global _scl_prefix %{ns_dir}
%global scl_name_base    %{ns_name}-php
%global scl_macro_base   %{ns_name}_php
%global scl_name_version 81
%global scl              %{scl_name_base}%{scl_name_version}
%scl_package %scl

Summary:       Package that installs PHP 8.1
Name:          %scl_name
Version:       8.1.34
Vendor:        cPanel, Inc.
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define        release_prefix 1
Release:       %{release_prefix}%{?dist}.cpanel
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README.md
Source2:       LICENSE
Source3:       whm_feature_addon

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}php-common
Requires:      %{?scl_prefix}php-cli

# Our code requires that pear be installed when the meta package is installed
Requires:      %{?scl_prefix}pear

%description
This is the main package for %scl Software Collection,
that install PHP 8.1 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

Provides:  ea-php-scldevel = %{version}
Conflicts: ea-php-scldevel > %{version}, ea-php-scldevel < %{version}

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_macro_base}         %{scl}
%%scl_prefix_%{scl_macro_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/etc
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/share/doc
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/include
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/share/man/man1
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/bin
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/var/cache
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/var/tmp
mkdir -p %{buildroot}/opt/cpanel/ea-php81/root/usr/%{_lib}
mkdir -p %{buildroot}/usr/local/cpanel/whostmgr/addonfeatures
install %{SOURCE3} %{buildroot}/usr/local/cpanel/whostmgr/addonfeatures/%{name}

# Even if this package doesn't use it we need to do this because if another
# package does (e.g. pear licenses) it will be created and unowned by any RPM
%if 0%{?_licensedir:1}
mkdir %{buildroot}/%{_licensedir}
%endif

%scl_install

tmp_version=$(echo %{scl_name_version} | sed -re 's/([0-9])([0-9])/\1\.\2/')
sed -e 's/@SCL@/%{scl_macro_base}%{scl_name_version}/g' -e "s/@VERSION@/${tmp_version}/g" %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

# Remove empty share/[man|locale]/ directories
find %{buildroot}/opt/cpanel/%{scl}/root/usr/share/man/ -type d -empty -delete
find %{buildroot}/opt/cpanel/%{scl}/root/usr/share/locale/ -type d -empty -delete
mkdir -p %{buildroot}/opt/cpanel/%{scl}/root/usr/share/locale

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files


%files runtime
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*
%dir /opt/cpanel/ea-php81/root/etc
%dir /opt/cpanel/ea-php81/root/usr
%dir /opt/cpanel/ea-php81/root/usr/share
%dir /opt/cpanel/ea-php81/root/usr/share/doc
%dir /opt/cpanel/ea-php81/root/usr/include
%dir /opt/cpanel/ea-php81/root/usr/share/man
%dir /opt/cpanel/ea-php81/root/usr/bin
%dir /opt/cpanel/ea-php81/root/usr/var
%dir /opt/cpanel/ea-php81/root/usr/var/cache
%dir /opt/cpanel/ea-php81/root/usr/var/tmp
%dir /opt/cpanel/ea-php81/root/usr/%{_lib}
%attr(644, root, root) /usr/local/cpanel/whostmgr/addonfeatures/%{name}
%if 0%{?_licensedir:1}
%dir %{_licensedir}
%endif

%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Thu Dec 18 2025 Dan Muey <daniel.muey@webpros.com> - 8.1.34-1
- EA-13298: Update ea-php81 from v8.1.33 to v8.1.34

* Thu Jul 03 2025 Cory McIntire <cory.mcintire@webpros.com> - 8.1.33-1
- EA-13001: Update ea-php81 from v8.1.32 to v8.1.33

* Thu Mar 13 2025 Cory McIntire <cory.mcintire@webpros.com> - 8.1.32-1
- EA-12766: Update ea-php81 from v8.1.31 to v8.1.32

* Thu Nov 21 2024 Cory McIntire <cory@cpanel.net> - 8.1.31-1
- EA-12576: Update ea-php81 from v8.1.30 to v8.1.31
- (Single byte overread with convert.quoted-printable-decode filter). (CVE-2024-11233)
- (Configuring a proxy in a stream context might allow for CRLF injection in URIs). (CVE-2024-11234)
- (Integer overflow in the dblib quoter causing OOB writes). (CVE-2024-11236)
- (Integer overflow in the firebird quoter causing OOB writes). (CVE-2024-11236)
- (Leak partial content of the heap through heap buffer over-read). (CVE-2024-8929)
- (OOB access in ldap_escape). (CVE-2024-8932)

* Thu Sep 26 2024 Cory McIntire <cory@cpanel.net> - 8.1.30-1
- EA-12428: Update ea-php81 from v8.1.29 to v8.1.30

* Thu Jun 06 2024 Cory McIntire <cory@cpanel.net> - 8.1.29-1
- EA-12192: Update ea-php81 from v8.1.28 to v8.1.29

* Fri Apr 12 2024 Cory McIntire <cory@cpanel.net> - 8.1.28-1
- EA-12087: Update ea-php81 from v8.1.27 to v8.1.28

* Tue Jan 02 2024 Travis Holloway <t.holloway@cpanel.net> - 8.1.27-1
- EA-11892: Update ea-php81 from v8.1.26 to v8.1.27

* Tue Nov 28 2023 Julian Brown <julian.brown@cpanel.net> - 8.1.26-2
- ZC-11419: Correct Ubuntu build issues

* Fri Nov 24 2023 Cory McIntire <cory@cpanel.net> - 8.1.26-1
- EA-11824: Update ea-php81 from v8.1.25 to v8.1.26

* Fri Oct 27 2023 Cory McIntire <cory@cpanel.net> - 8.1.25-1
- EA-11776: Update ea-php81 from v8.1.24 to v8.1.25

* Mon Oct 02 2023 Cory McIntire <cory@cpanel.net> - 8.1.24-1
- EA-11716: Update ea-php81 from v8.1.23 to v8.1.24

* Fri Sep 08 2023 Cory McIntire <cory@cpanel.net> - 8.1.23-1
- EA-11664: Update ea-php81 from v8.1.22 to v8.1.23

* Thu Aug 03 2023 Cory McIntire <cory@cpanel.net> - 8.1.22-1
- EA-11589: Update ea-php81 from v8.1.21 to v8.1.22

* Fri Jul 07 2023 Cory McIntire <cory@cpanel.net> - 8.1.21-1
- EA-11538: Update ea-php81 from v8.1.20 to v8.1.21

* Thu Jun 08 2023 Cory McIntire <cory@cpanel.net> - 8.1.20-1
- EA-11477: Update ea-php81 from v8.1.19 to v8.1.20

* Mon May 16 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 8.1.19-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Fri May 12 2023 Cory McIntire <cory@cpanel.net> - 8.1.19-1
- EA-11415: Update ea-php81 from v8.1.18 to v8.1.19

* Fri Apr 14 2023 Cory McIntire <cory@cpanel.net> - 8.1.18-1
- EA-11356: Update ea-php81 from v8.1.17 to v8.1.18

* Thu Mar 16 2023 Cory McIntire <cory@cpanel.net> - 8.1.17-1
- EA-11300: Update ea-php81 from v8.1.16 to v8.1.17

* Wed Feb 15 2023 Cory McIntire <cory@cpanel.net> - 8.1.16-1
- EA-11244: Update ea-php81 from v8.1.15 to v8.1.16

* Fri Feb 03 2023 Cory McIntire <cory@cpanel.net> - 8.1.15-1
- EA-11208: Update ea-php81 from v8.1.14 to v8.1.15

* Thu Jan 05 2023 Cory McIntire <cory@cpanel.net> - 8.1.14-1
- EA-11133: Update ea-php81 from v8.1.13 to v8.1.14

* Thu Nov 24 2022 Cory McIntire <cory@cpanel.net> - 8.1.13-1
- EA-11070: Update ea-php81 from v8.1.12 to v8.1.13

* Fri Oct 28 2022 Cory McIntire <cory@cpanel.net> - 8.1.12-1
- EA-11021: Update ea-php81 from v8.1.11 to v8.1.12

* Thu Sep 29 2022 Cory McIntire <cory@cpanel.net> - 8.1.11-1
- EA-10958: Update ea-php81 from v8.1.10 to v8.1.11

* Thu Sep 01 2022 Cory McIntire <cory@cpanel.net> - 8.1.10-1
- EA-10916: Update ea-php81 from v8.1.9 to v8.1.10

* Thu Aug 04 2022 Cory McIntire <cory@cpanel.net> - 8.1.9-1
- EA-10865: Update ea-php81 from v8.1.8 to v8.1.9

* Thu Jul 07 2022 Cory McIntire <cory@cpanel.net> - 8.1.8-1
- EA-10821: Update ea-php81 from v8.1.7 to v8.1.8

* Thu Jun 09 2022 Cory McIntire <cory@cpanel.net> - 8.1.7-1
- EA-10758: Update ea-php81 from v8.1.6 to v8.1.7

* Thu May 12 2022 Cory McIntire <cory@cpanel.net> - 8.1.6-1
- EA-10705: Update ea-php81 from v8.1.5 to v8.1.6

* Thu Apr 14 2022 Cory McIntire <cory@cpanel.net> - 8.1.5-1
- EA-10634: Update ea-php81 from v8.1.4 to v8.1.5

* Thu Mar 17 2022 Cory McIntire <cory@cpanel.net> - 8.1.4-1
- EA-10577: Update ea-php81 from v8.1.3 to v8.1.4

* Fri Feb 18 2022 Cory McIntire <cory@cpanel.net> - 8.1.3-1
- EA-10506: Update ea-php81 from v8.1.2 to v8.1.3

* Fri Jan 21 2022 Tim Mullin <tim@cpanel.net> - 8.1.2-1
- EA-10451: Update ea-php81 from v8.1.1 to v8.1.2

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 8.1.1-2
- ZC-9589: Update DISABLE_BUILD to match OBS

* Fri Dec 17 2021 Cory McIntire <cory@cpanel.net> - 8.1.1-1
- EA-10366: Update ea-php81 from v8.1.0 to v8.1.1

* Tue Nov 23 2021 Julian Brown <julian.brown@webpros.com> - 8.1.0-1
- ZC-8524: Build of release

* Thu Nov 04 2021 Julian Brown <julian.brown@webpros.com> - 8.1.0rc6-1
- ZC-8130: First build of php8.1

