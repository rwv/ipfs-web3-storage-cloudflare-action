cloudflare_record=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?type=TXT&name=_dnslink.$DOMAIN" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json")
if [[ ${cloudflare_record} == *"\"success\":false"* ]]; then
  echo ${cloudflare_record}
  echo "Error! Can't get $DOMAIN record inforamiton from cloudflare API"
  exit 0
fi

cloudflare_record_id=$(echo $cloudflare_record | jq '.result[0].id' | sed 's/"//g')

echo "Cloudflare Record ID: $cloudflare_record_id"

final_result=$(curl -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$cloudflare_record_id" \
     -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
     -H "Content-Type: application/json" \
     --data "{\"type\":\"TXT\",\"name\":\"_dnslink.$DOMAIN\",\"content\":\"dnslink=/ipfs/$CID\",\"ttl\":1,\"proxied\":false}")

echo "Final Result: $final_result"

exit 0