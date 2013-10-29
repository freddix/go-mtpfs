Summary:	Simple FUSE filesystem for mounting Android devices
Name:		go-mtpfs
Version:	20131022
Release:	1
License:	BSD
Group:		Applications
Source0:	https://github.com/hanwen/go-mtpfs/archive/master.zip
# Source0-md5:	22168f37af0cf88d3dc7681f788af5f5
URL:		https://github.com/hanwen/go-mtpfs
BuildRequires:	fuse-devel
BuildRequires:	gcc-go
BuildRequires:	libusbx-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Go-mtpfs is a simple FUSE filesystem for mounting Android devices as a
MTP device.

It will expose all storage areas of a device in the mount, and only
reads file metadata as needed, making it mount quickly. It uses
Android extensions to read/write partial data, so manipulating large
files requires no extra space in /tmp.

%prep
%setup -qn %{name}-master

%build
GOPATH=/home/users/builder/rpm/BUILD/%{name}-master go get -v -x github.com/hanwen/go-mtpfs

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%if %{with ldconfig}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%endif

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO

%if 0
# if _sysconfdir != /etc:
#%%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%endif

# initscript and its config
%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif

#%{_examplesdir}/%{name}-%{version}

%if %{with subpackage}
%files subpackage
%defattr(644,root,root,755)
#%doc extras/*.gz
#%{_datadir}/%{name}-ext
%endif
