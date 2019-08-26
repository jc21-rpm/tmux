%define debug_package %{nil}

%global gh_user    tmux
%global gh_version 2.9a

Name:           tmux
Version:        2.9.1
Release:        1
Summary:        A terminal multiplexer
Group:          Applications/System
License:        ISC and BSD
URL:            https://tmux.github.io/
BuildRequires:  ncurses-devel
BuildRequires:  libevent-devel
BuildRequires:  libutempter-devel
Source1:        bash_completion_tmux.sh

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
wget https://github.com/%{gh_user}/%{name}/archive/%{gh_version}.tar.gz
tar xzf %{gh_version}.tar.gz


%build
FLAGS="$RPM_OPT_FLAGS -fPIC -pie -Wl,-z,relro -Wl,-z,now"
CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie -Wl,-z,relro -Wl,-z,now"
export CFLAGS
export CXXFLAGS
mv %{name}-%{gh_version} %{name}-%{version}
cd %{name}-%{version}
%configure
make %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
make install DESTDIR=%{buildroot} INSTALLBIN="install -p -m 755" INSTALLMAN="install -p -m 644"
# bash completion
install -Dpm 644 %{SOURCE1} %{buildroot}%{_datadir}/bash-completion/completions/tmux

%post
if [ "$1" = 1 ]; then
  if [ ! -f %{_sysconfdir}/shells ] ; then
    touch %{_sysconfdir}/shells
  fi
  for binpath in %{_bindir} /bin; do
    if ! grep -q "^${binpath}/tmux$" %{_sysconfdir}/shells; then
       (cat %{_sysconfdir}/shells; echo "$binpath/tmux") > %{_sysconfdir}/shells.new
       mv %{_sysconfdir}/shells{.new,}
    fi
  done
fi

%postun
if [ "$1" = 0 ] && [ -f %{_sysconfdir}/shells ] ; then
  sed -e '\!^%{_bindir}/tmux$!d' -e '\!^/bin/tmux$!d' < %{_sysconfdir}/shells > %{_sysconfdir}/shells.new
  mv %{_sysconfdir}/shells{.new,}
fi

%clean
rm -rf %{buildroot}

%files
%doc CHANGES FAQ TODO
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*
%{_datadir}/bash-completion/completions/tmux

%changelog
* Mon Aug 26 2019 Jamie Curnow <jc@jc21.com> 2.9.1-1
- v2.9a

