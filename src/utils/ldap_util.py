import ldap

l = ldap.initialize('')
l.protocol_version = ldap.VERSION3
l.simple_bind_s('','')
l.search_s('',ldap.SCOPE_SUBTREE,'(sAMAccountName=wang)',None)