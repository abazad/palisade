<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output method="html"/>
	<xsl:template match="/">
		<html>
			<body>					
				<xsl:for-each select="Employee">
					<h2><xsl:value-of select="./@USER_NAME"/></h2>
					<table border="1">
						<tr bgcolor="#9acd32">
							<th>URL</th>
							<th>Bytes</th>
						</tr>
						<xsl:for-each select="ROW">
							<tr>
								<td><xsl:value-of select="URL_HOSTNAME"/></td>
								<td><xsl:value-of select="BYTES"/></td>
							</tr>
						</xsl:for-each>
					</table>
				</xsl:for-each>			
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>