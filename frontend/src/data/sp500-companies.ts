export interface Company {
  name: string;
  ticker: string;
  aliases?: string[];
}

// S&P 500 companies with major representatives from each sector
export const SP500_COMPANIES: Company[] = [
  // Technology
  { name: "Apple Inc.", ticker: "AAPL", aliases: ["Apple", "Apple Computer"] },
  { name: "Microsoft Corporation", ticker: "MSFT", aliases: ["Microsoft", "MS"] },
  { name: "Amazon.com Inc.", ticker: "AMZN", aliases: ["Amazon", "Amazon.com"] },
  { name: "NVIDIA Corporation", ticker: "NVDA", aliases: ["NVIDIA", "Nvidia"] },
  { name: "Alphabet Inc.", ticker: "GOOGL", aliases: ["Google", "Alphabet"] },
  { name: "Meta Platforms Inc.", ticker: "META", aliases: ["Facebook", "Meta", "Meta Platforms"] },
  { name: "Tesla Inc.", ticker: "TSLA", aliases: ["Tesla", "Tesla Motors"] },
  { name: "Oracle Corporation", ticker: "ORCL", aliases: ["Oracle"] },
  { name: "Adobe Inc.", ticker: "ADBE", aliases: ["Adobe", "Adobe Systems"] },
  { name: "Salesforce Inc.", ticker: "CRM", aliases: ["Salesforce", "Salesforce.com"] },
  { name: "Cisco Systems Inc.", ticker: "CSCO", aliases: ["Cisco", "Cisco Systems"] },
  { name: "Intel Corporation", ticker: "INTC", aliases: ["Intel"] },
  { name: "Advanced Micro Devices Inc.", ticker: "AMD", aliases: ["AMD", "Advanced Micro Devices"] },
  { name: "Qualcomm Incorporated", ticker: "QCOM", aliases: ["Qualcomm"] },
  { name: "Broadcom Inc.", ticker: "AVGO", aliases: ["Broadcom"] },
  { name: "Texas Instruments Incorporated", ticker: "TXN", aliases: ["Texas Instruments", "TI"] },
  { name: "Applied Materials Inc.", ticker: "AMAT", aliases: ["Applied Materials"] },
  { name: "Lam Research Corporation", ticker: "LRCX", aliases: ["Lam Research"] },
  { name: "Micron Technology Inc.", ticker: "MU", aliases: ["Micron"] },
  { name: "NXP Semiconductors N.V.", ticker: "NXPI", aliases: ["NXP", "NXP Semiconductors"] },
  { name: "Marvell Technology Inc.", ticker: "MRVL", aliases: ["Marvell", "Marvell Technology"] },
  { name: "Analog Devices Inc.", ticker: "ADI", aliases: ["Analog Devices", "ADI"] },
  { name: "Synopsys Inc.", ticker: "SNPS", aliases: ["Synopsys"] },
  { name: "Cadence Design Systems Inc.", ticker: "CDNS", aliases: ["Cadence"] },
  { name: "Intuit Inc.", ticker: "INTU", aliases: ["Intuit"] },
  { name: "Autodesk Inc.", ticker: "ADSK", aliases: ["Autodesk"] },
  { name: "Workday Inc.", ticker: "WDAY", aliases: ["Workday"] },
  { name: "ServiceNow Inc.", ticker: "NOW", aliases: ["ServiceNow"] },
  { name: "Snowflake Inc.", ticker: "SNOW", aliases: ["Snowflake"] },
  { name: "Datadog Inc.", ticker: "DDOG", aliases: ["Datadog"] },
  { name: "CrowdStrike Holdings Inc.", ticker: "CRWD", aliases: ["CrowdStrike"] },
  { name: "Palo Alto Networks Inc.", ticker: "PANW", aliases: ["Palo Alto Networks"] },
  { name: "Fortinet Inc.", ticker: "FTNT", aliases: ["Fortinet"] },
  { name: "Zscaler Inc.", ticker: "ZS", aliases: ["Zscaler"] },
  { name: "Okta Inc.", ticker: "OKTA", aliases: ["Okta"] },
  { name: "Splunk Inc.", ticker: "SPLK", aliases: ["Splunk"] },
  { name: "Dell Technologies Inc.", ticker: "DELL", aliases: ["Dell", "Dell Technologies"] },
  { name: "HP Inc.", ticker: "HPQ", aliases: ["HP", "Hewlett-Packard"] },
  { name: "IBM Corporation", ticker: "IBM", aliases: ["IBM", "International Business Machines"] },
  { name: "Netflix Inc.", ticker: "NFLX", aliases: ["Netflix"] },
  
  // Financial Services
  { name: "Berkshire Hathaway Inc.", ticker: "BRK.B", aliases: ["Berkshire Hathaway", "Berkshire"] },
  { name: "JPMorgan Chase & Co.", ticker: "JPM", aliases: ["JPMorgan", "JP Morgan", "JPMorgan Chase"] },
  { name: "Bank of America Corp.", ticker: "BAC", aliases: ["Bank of America", "BofA", "BOA"] },
  { name: "Wells Fargo & Company", ticker: "WFC", aliases: ["Wells Fargo"] },
  { name: "Goldman Sachs Group Inc.", ticker: "GS", aliases: ["Goldman Sachs", "Goldman"] },
  { name: "Morgan Stanley", ticker: "MS", aliases: ["Morgan Stanley"] },
  { name: "American Express Company", ticker: "AXP", aliases: ["American Express", "Amex"] },
  { name: "Visa Inc.", ticker: "V", aliases: ["Visa"] },
  { name: "Mastercard Inc.", ticker: "MA", aliases: ["Mastercard", "MasterCard"] },
  { name: "PayPal Holdings Inc.", ticker: "PYPL", aliases: ["PayPal"] },
  
  // Healthcare
  { name: "UnitedHealth Group Inc.", ticker: "UNH", aliases: ["UnitedHealth", "United Health"] },
  { name: "Johnson & Johnson", ticker: "JNJ", aliases: ["J&J", "Johnson and Johnson"] },
  { name: "Merck & Co. Inc.", ticker: "MRK", aliases: ["Merck", "Merck & Co"] },
  { name: "Pfizer Inc.", ticker: "PFE", aliases: ["Pfizer"] },
  { name: "AbbVie Inc.", ticker: "ABBV", aliases: ["AbbVie"] },
  { name: "Eli Lilly and Company", ticker: "LLY", aliases: ["Eli Lilly", "Lilly"] },
  { name: "Abbott Laboratories", ticker: "ABT", aliases: ["Abbott"] },
  { name: "Bristol-Myers Squibb Company", ticker: "BMY", aliases: ["Bristol-Myers Squibb", "BMS"] },
  { name: "Amgen Inc.", ticker: "AMGN", aliases: ["Amgen"] },
  { name: "Gilead Sciences Inc.", ticker: "GILD", aliases: ["Gilead", "Gilead Sciences"] },
  { name: "Regeneron Pharmaceuticals Inc.", ticker: "REGN", aliases: ["Regeneron"] },
  { name: "Vertex Pharmaceuticals Incorporated", ticker: "VRTX", aliases: ["Vertex", "Vertex Pharmaceuticals"] },
  { name: "Moderna Inc.", ticker: "MRNA", aliases: ["Moderna"] },
  { name: "Biogen Inc.", ticker: "BIIB", aliases: ["Biogen"] },
  
  // Consumer Goods
  { name: "Walmart Inc.", ticker: "WMT", aliases: ["Walmart", "Wal-Mart"] },
  { name: "The Coca-Cola Company", ticker: "KO", aliases: ["Coca-Cola", "Coke"] },
  { name: "PepsiCo Inc.", ticker: "PEP", aliases: ["Pepsi", "PepsiCo"] },
  { name: "Procter & Gamble Co.", ticker: "PG", aliases: ["P&G", "Procter and Gamble"] },
  { name: "Nike Inc.", ticker: "NKE", aliases: ["Nike"] },
  { name: "The Home Depot Inc.", ticker: "HD", aliases: ["Home Depot", "The Home Depot"] },
  { name: "Costco Wholesale Corporation", ticker: "COST", aliases: ["Costco", "Costco Wholesale"] },
  { name: "Target Corporation", ticker: "TGT", aliases: ["Target"] },
  { name: "Lowe's Companies Inc.", ticker: "LOW", aliases: ["Lowe's", "Lowes"] },
  { name: "McDonald's Corporation", ticker: "MCD", aliases: ["McDonald's", "McDonalds"] },
  { name: "Starbucks Corporation", ticker: "SBUX", aliases: ["Starbucks"] },
  { name: "The Walt Disney Company", ticker: "DIS", aliases: ["Disney", "Walt Disney"] },
  
  // Energy
  { name: "Exxon Mobil Corporation", ticker: "XOM", aliases: ["Exxon", "ExxonMobil", "Exxon Mobil"] },
  { name: "Chevron Corporation", ticker: "CVX", aliases: ["Chevron"] },
  { name: "ConocoPhillips", ticker: "COP", aliases: ["ConocoPhillips", "Conoco Phillips"] },
  { name: "EOG Resources Inc.", ticker: "EOG", aliases: ["EOG Resources", "EOG"] },
  { name: "Schlumberger Limited", ticker: "SLB", aliases: ["Schlumberger"] },
  { name: "Marathon Petroleum Corporation", ticker: "MPC", aliases: ["Marathon Petroleum", "Marathon"] },
  { name: "Valero Energy Corporation", ticker: "VLO", aliases: ["Valero"] },
  { name: "Phillips 66", ticker: "PSX", aliases: ["Phillips 66"] },
  
  // Industrial
  { name: "Boeing Company", ticker: "BA", aliases: ["Boeing"] },
  { name: "Caterpillar Inc.", ticker: "CAT", aliases: ["Caterpillar"] },
  { name: "3M Company", ticker: "MMM", aliases: ["3M"] },
  { name: "General Electric Company", ticker: "GE", aliases: ["GE", "General Electric"] },
  { name: "Honeywell International Inc.", ticker: "HON", aliases: ["Honeywell"] },
  { name: "United Parcel Service Inc.", ticker: "UPS", aliases: ["UPS", "United Parcel Service"] },
  { name: "FedEx Corporation", ticker: "FDX", aliases: ["FedEx", "Federal Express"] },
  { name: "Deere & Company", ticker: "DE", aliases: ["John Deere", "Deere"] },
  { name: "General Motors Company", ticker: "GM", aliases: ["GM", "General Motors"] },
  { name: "Ford Motor Company", ticker: "F", aliases: ["Ford"] },
  { name: "Raytheon Technologies Corporation", ticker: "RTX", aliases: ["Raytheon", "Raytheon Technologies"] },
  { name: "Lockheed Martin Corporation", ticker: "LMT", aliases: ["Lockheed Martin", "Lockheed"] },
  { name: "Northrop Grumman Corporation", ticker: "NOC", aliases: ["Northrop Grumman", "Northrop"] },
  
  // Airlines
  { name: "Delta Air Lines Inc.", ticker: "DAL", aliases: ["Delta", "Delta Air Lines"] },
  { name: "American Airlines Group Inc.", ticker: "AAL", aliases: ["American Airlines", "AA"] },
  { name: "United Airlines Holdings Inc.", ticker: "UAL", aliases: ["United Airlines", "United"] },
  { name: "Southwest Airlines Co.", ticker: "LUV", aliases: ["Southwest Airlines", "Southwest"] },
  
  // Telecommunications
  { name: "Verizon Communications Inc.", ticker: "VZ", aliases: ["Verizon"] },
  { name: "AT&T Inc.", ticker: "T", aliases: ["AT&T", "ATT"] },
  { name: "Comcast Corporation", ticker: "CMCSA", aliases: ["Comcast"] },
  { name: "T-Mobile US Inc.", ticker: "TMUS", aliases: ["T-Mobile", "T-Mobile US"] },
  
  // Utilities
  { name: "NextEra Energy Inc.", ticker: "NEE", aliases: ["NextEra Energy", "NextEra"] },
  { name: "Duke Energy Corporation", ticker: "DUK", aliases: ["Duke Energy", "Duke"] },
  { name: "Southern Company", ticker: "SO", aliases: ["Southern Company", "Southern"] },
  { name: "Dominion Energy Inc.", ticker: "D", aliases: ["Dominion Energy", "Dominion"] },
  
  // Real Estate
  { name: "American Tower Corporation", ticker: "AMT", aliases: ["American Tower"] },
  { name: "Prologis Inc.", ticker: "PLD", aliases: ["Prologis"] },
  { name: "Equinix Inc.", ticker: "EQIX", aliases: ["Equinix"] },
  { name: "Public Storage", ticker: "PSA", aliases: ["Public Storage"] },
  
  // Materials
  { name: "Linde plc", ticker: "LIN", aliases: ["Linde"] },
  { name: "Air Products and Chemicals Inc.", ticker: "APD", aliases: ["Air Products", "Air Products and Chemicals"] },
  { name: "Sherwin-Williams Company", ticker: "SHW", aliases: ["Sherwin-Williams", "Sherwin Williams"] },
  { name: "Freeport-McMoRan Inc.", ticker: "FCX", aliases: ["Freeport-McMoRan", "Freeport"] },
  
  // Consumer Staples
  { name: "Walmart Inc.", ticker: "WMT", aliases: ["Walmart", "Wal-Mart"] },
  { name: "Costco Wholesale Corporation", ticker: "COST", aliases: ["Costco", "Costco Wholesale"] },
  { name: "Kroger Co.", ticker: "KR", aliases: ["Kroger"] },
  { name: "Walgreens Boots Alliance Inc.", ticker: "WBA", aliases: ["Walgreens", "Walgreens Boots Alliance"] },
  { name: "Mondelez International Inc.", ticker: "MDLZ", aliases: ["Mondelez", "Mondelez International"] },
  { name: "General Mills Inc.", ticker: "GIS", aliases: ["General Mills"] },
  { name: "Kellogg Company", ticker: "K", aliases: ["Kellogg"] },
  { name: "Kraft Heinz Company", ticker: "KHC", aliases: ["Kraft Heinz", "Kraft", "Heinz"] },
];
