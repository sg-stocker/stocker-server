package capstone1.stocker.application;

import capstone1.stocker.dto.Oauth2Token;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
@Service
@Slf4j
public class Oath2Service {

    private Oauth2Token oauth2Token;

    @Value("${APP_Key}")
    private String appKey;
    @Value("${APP_SECRET}")
    private String appSecret;

    public String getAccessToken() throws JsonProcessingException, JSONException {
        if(oauth2Token == null || oauth2Token.isExpired()){
            oauth2Token = fetchNewToken();
        }

        return oauth2Token.getAccess_token();
    }

    public Oauth2Token fetchNewToken() throws JsonProcessingException, JSONException {
        RestTemplate restTemplate = new RestTemplate();

        String url = "https://openapivts.koreainvestment.com:29443/oauth2/tokenP";
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);

        JSONObject body = new JSONObject();
        body.put("grant_type", "client_credentials");
        body.put("appkey",appKey);
        body.put("appsecret", appSecret);


        HttpEntity<?> requestMessage = new HttpEntity<>(body.toString(), httpHeaders);
        HttpEntity<String> response= restTemplate.postForEntity(
                url,
                requestMessage,
                String.class);


        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.configure(DeserializationFeature.ACCEPT_EMPTY_STRING_AS_NULL_OBJECT, true);
        return objectMapper.readValue(response.getBody(), Oauth2Token.class);

    }
}
