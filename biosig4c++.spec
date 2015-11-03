Name:           biosig4c++
Version:        1.7.2
Release:        1%{?dist}
Summary:        I/O library for biomedical data

License:        GPLv3+
URL:            http://biosig.sourceforge.net/
Source0:        http://downloads.sourceforge.net/biosig/src/biosig4c++-%{version}.src.tar.gz

BuildRequires:  make
BuildRequires:  gcc gcc-c++
BuildRequires:  suitesparse-devel
BuildRequires:  zlib-devel
BuildRequires:  octave-devel

%description
%{summary}.

%prep
%autosetup
echo '#!/bin/sh' > ./configure
chmod +x ./configure

%build
%configure
sed -i \
  -e '/$(DESTDIR)$(prefix)\/lib/s/lib/%{_lib}/' \
  -e 's,\(prefix[ \t]*:= \)/usr/local,\1/%{_prefix},' \
  -e 's,libdir=$(prefix)/lib,libdir=%{_libdir},' \
  -e 's,-L$(prefix)/lib,-L%{_libdir},' \
  Makefile
export MAKEOPTS='LIBEXT=so prefix=%{_prefix}'
%make_build $MAKEOPTS libbiosig
cp -p libbiosig.pc libbiosig.pc.tmp
sed -i -e 's|-L%{_libdir}|-L.|' libbiosig.pc
export PKG_CONFIG_PATH="`pwd`:$PKG_CONFIG_PATH"
%make_build $MAKEOPTS save2gdf
%make_build $MAKEOPTS mex4o
mv libbiosig.pc.tmp libbiosig.pc
#make_build $MAKEOPTS biosig4python

%install
%make_install 
mkdir -p %{buildroot}%{_bindir}
install -p -m0755 save2gdf  %{buildroot}%{_bindir}/
install -p -m0755 heka2itx  %{buildroot}%{_bindir}/
install -p -m0755 save2aecg %{buildroot}%{_bindir}/
install -p -m0755 save2scp  %{buildroot}%{_bindir}/
#make install_octave
find %{buildroot} -name '*.a' -delete

%files
%license LICENSE
%doc

%changelog
* Tue Nov 03 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.2-1
- Initial package

