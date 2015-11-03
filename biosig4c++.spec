Name:           biosig4c++
Version:        1.7.2
Release:        1%{?dist}
Summary:        I/O library for biomedical data

License:        GPLv3+
URL:            http://biosig.sourceforge.net/
Source0:        http://downloads.sourceforge.net/biosig/src/biosig4c++-%{version}.src.tar.gz
Patch0:         biosig-makefile.patch
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  gcc gcc-c++
BuildRequires:  suitesparse-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
BuildRequires:  octave-devel
BuildRequires:  hdf5-devel
BuildRequires:  dcmtk-devel

%description
%{summary}.

%package tools
Summary:        Format conversion tools for biomedical data formats
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
Based on BioSig library, this package provides command line tools, such as
- save2gdf: converter between different file formats, including but
  not limited to SCP-ECG(EN1064), HL7aECG (FDA-XML), GDF, EDF, BDF,
  CWFB.  save2gdf can be also used to upload or retrieve data from a
  bscs server.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.

%prep
%autosetup -S git
echo '#!/bin/sh' > ./configure
chmod +x ./configure
# Drop bundled TinyXML
rm -vrf XMLParser/

%build
%configure
sed -i \
  -e 's,@LIBDIR@,%{_libdir},' \
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
# TODO: octave bindings
#make_build $MAKEOPTS mex4o oct
# TODO: pyhton bindings
#make_build $MAKEOPTS biosig4python
mv libbiosig.pc.tmp libbiosig.pc

%install
%make_install 
mkdir -p %{buildroot}%{_bindir}
install -p -m0755 save2gdf  %{buildroot}%{_bindir}/
install -p -m0755 heka2itx  %{buildroot}%{_bindir}/
install -p -m0755 save2aecg %{buildroot}%{_bindir}/
install -p -m0755 save2scp  %{buildroot}%{_bindir}/

find %{buildroot} -name '*.a' -delete

%files
%license LICENSE
%{_libdir}/libbiosig*.so.*
%{_libdir}/libgdftime.so
%{_libdir}/libphysicalunits.so

%files tools
%{_bindir}/save2gdf
%{_bindir}/heka2itx
%{_bindir}/save2aecg
%{_bindir}/save2scp

%files devel
%{_includedir}/biosig*.h
%{_includedir}/gdftime.h
%{_includedir}/physicalunits.h
%{_libdir}/libbiosig*.so
%{_libdir}/pkgconfig/libbiosig.pc

%changelog
* Tue Nov 03 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.2-1
- Initial package
