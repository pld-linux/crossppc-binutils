#

Summary:	Cross PPC GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - PPC binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - PPC binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla PPC - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - PPC binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - PPC binutils
Name:		crossppc-binutils
Version:	2.20.51.0.3
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	ftp://ftp.kernel.org/pub/linux/devel/binutils/binutils-%{version}.tar.bz2
# Source0-md5:	4d5cdcfa054e697ba92a37f55b125080
Source1:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/binutils-non-english-man-pages.tar.bz2
# Source1-md5:	a717d9707ec77d82acb6ec9078c472d6
Patch0:		binutils-gasp.patch
Patch1:		binutils-info.patch
Patch2:		binutils-libtool-relink.patch
Patch3:		binutils-pt_pax_flags.patch
Patch5:		binutils-flex.patch
Patch6:		binutils-discarded.patch
Patch7:		binutils-absolute-gnu_debuglink-path.patch
Patch8:		binutils-libtool-m.patch
Patch9:		binutils-build-id.patch
Patch10:	binutils-tooldir.patch
URL:		http://sources.redhat.com/binutils/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel >= 6:4.0-1
BuildRequires:	perl-tools-pod
%ifarch sparc sparc32
BuildRequires:	sparc32
%endif
BuildRequires:	texinfo >= 4.2
Conflicts:	gcc-c++ < 5:3.3
ExcludeArch:	ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		ppc-pld-linux
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for PPC.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla PPC.

%prep
%setup -q -n binutils-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{?with_pax:%patch3 -p1}
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# file contains hacks for ac 2.59 only
rm config/override.m4

%build
%{__aclocal}
%{__autoconf}

# non-standard regeneration (needed because of gasp patch)
# AM_BINUTILS_WARNINGS in bfd/warning.m4, ZW_GNU_GETTEXT_SISTER_DIR in config/gettext-sister.m4
for dir in gas bfd; do
	cd $dir || exit 1
	%{__aclocal} -I .. -I ../config -I ../bfd
	%{__automake} Makefile
	%{__automake} doc/Makefile
	%{__autoconf}
	cd ..
done

cp -f /usr/share/automake/config.* .

CFLAGS="%{rpmcflags}"; export CFLAGS
CC="%{__cc}"; export CC
%ifarch sparc
sparc32 \
%endif
./configure %{_target_platform} \
	--disable-debug \
	--disable-werror \
	--enable-build-warnings=,-Wno-missing-prototypes \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--with-tooldir=%{arch} \
	--enable-gold=both \
	--target=%{target}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_infodir}/standards.info*

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%{arch}/lib/ldscripts
%{_mandir}/man?/%{target}-*
