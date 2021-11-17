#!/bin/bash

source debian/vars.sh

set -x

[ "$DEB_INSTALL_ROOT" != "/" ] && rm -rf $DEB_INSTALL_ROOT
install -D -m 644 enable $DEB_INSTALL_ROOT$_scl_scripts/enable
install -D -m 644 scldev $DEB_INSTALL_ROOT$_root_sysconfdir/rpm/macros.$scl_name_base-scldevel
install -D -m 644 $scl_name.7 $DEB_INSTALL_ROOT$_mandir/man7/$scl_name.7
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/etc
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/share/doc
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/include
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/share/man/man1
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/bin
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/var/cache
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/var/tmp
mkdir -p $DEB_INSTALL_ROOT/opt/cpanel/ea-php81/root/usr/$_lib
mkdir -p $DEB_INSTALL_ROOT/usr/local/cpanel/whostmgr/addonfeatures
install $SOURCE3 $DEB_INSTALL_ROOT/usr/local/cpanel/whostmgr/addonfeatures/$name
# Even if this package doesn't use it we need to do this because if another
# package does (e.g. pear licenses) it will be created and unowned by any RPM
mkdir $DEB_INSTALL_ROOT/$_licensedir
