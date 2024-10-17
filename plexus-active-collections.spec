%define project_version 1.0-beta-2

Name:           plexus-active-collections
Version:        1.0
Release:        0.3.beta2
Summary:        Plexus Container-Backed Active Collections

Group:          Development/Java
License:        ASL 2.0
URL:            https://plexus.codehaus.org/
#svn export http://svn.codehaus.org/plexus/tags/plexus-active-collections-1.0-beta-2/
#tar zcf plexus-active-collections-1.0-beta-2.tar.gz plexus-active-collections-1.0-beta-2/
Source0:        plexus-active-collections-1.0-beta-2.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

BuildRequires:  java >= 0:1.6.0
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant, ant-nodeps
BuildRequires:  maven2 >= 0:2.0.4-9
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven2-plugin-site
BuildRequires:  maven2-plugin-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven-shared-reporting-impl
BuildRequires:  maven-shared-plugin-testing-harness
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  plexus-maven-plugin
BuildRequires:  plexus-component-api
BuildRequires:  plexus-container-default
BuildRequires:  junit

Requires:          java >= 0:1.6.0
Requires:          plexus-component-api
Requires:          plexus-container-default
Requires:          plexus-utils
Requires:          junit
Requires:          jpackage-utils
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2


%description
Plexus Container-Backed Active Collections

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

Requires:          plexus-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}-%{project_version}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}/plexus
install -m 644 target/%{name}-%{project_version}.jar %{buildroot}%{_javadir}/plexus

(cd %{buildroot}%{_javadir}/plexus && for jar in *-%{project_version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{project_version}||g"`; done)

%add_to_maven_depmap org.codehaus.plexus %{name} %{project_version} JPP/plexus %{name}

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP.plexus-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/plexus/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/plexus/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/plexus/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/plexus/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/plexus/%{name}-%{version}
%{_javadocdir}/plexus/%{name}

