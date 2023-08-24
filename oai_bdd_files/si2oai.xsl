<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd" version="2.0">
  <!-- https://oai.cairn.info/oai.php?verb=ListRecords&metadataPrefix=oai_dc&set=AFCO -->
  <xsl:output method="xml" indent="yes"/>
  <xsl:template match="/*">
    <OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
      <responseDate>
        <xsl:value-of select="current-dateTime()"/>
      </responseDate>
      <request verb="ListRecords" metadataPrefix="oai_dc" set="BDD">https://api-scd.univ-cotedazur.fr/si-scd-middleware/oai</request>
      <ListRecords>
        <xsl:for-each select="item">
          <record>
            <header>
              <identifier>oai:bdd:<xsl:value-of select="bdd_id"/>
                     </identifier>
              <datestamp>2021-11-09</datestamp>
              <setSpec>BDD</setSpec>
            </header>
            <metadata>
              <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
                <dc:identifier>
                  <xsl:value-of select="bdd_id"/>
                </dc:identifier>
                <dc:title>
                  <xsl:value-of select="nom_court"/>
                </dc:title>
              </oai_dc:dc>
            </metadata>
          </record>
        </xsl:for-each>
      </ListRecords>
    </OAI-PMH>
  </xsl:template>
</xsl:stylesheet>
