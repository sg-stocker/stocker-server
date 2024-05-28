package capstone1.stocker.application;

import capstone1.stocker.dto.ChartResponseDto;
import capstone1.stocker.repository.CompanyRepository;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.web.util.UriComponentsBuilder;

@Service
@Slf4j
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class ChartService {
    private final Oath2Service oath2Service;
    private final CompanyRepository companyRepository;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd");

    @Value("${APP_Key}")
    private String appKey;
    @Value("${APP_SECRET}")
    private String appSecret;

    public ChartResponseDto getChart(String ticker) throws Exception {

        if (!companyRepository.existsByTicker(ticker)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "NO TICKERS");
        }

        RestTemplate restTemplate = new RestTemplate();

        String baseUrl = "https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice";

        // Header
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);
        httpHeaders.set("authorization", "Bearer " + oath2Service.getAccessToken());
        httpHeaders.set("appkey",appKey);
        httpHeaders.set("appsecret", appSecret);
        httpHeaders.set("tr_id", "FHKST03010100");
        httpHeaders.set("custtype", "P");

        // Query Parameter
        Map<String, String> queryParams = new HashMap<>();
        queryParams.put("FID_COND_MRKT_DIV_CODE", "J");
        queryParams.put("FID_INPUT_ISCD", ticker);


        // 날짜 계산
        LocalDateTime lastTime = LocalDateTime.now();
        LocalDateTime firstTime = lastTime.minusMonths(3);
        String formattedLast = lastTime.format(formatter);
        String formattedFirst = firstTime.format(formatter);

        queryParams.put("FID_INPUT_DATE_1", formattedFirst);
        queryParams.put("FID_INPUT_DATE_2", formattedLast);
        queryParams.put("FID_PERIOD_DIV_CODE", "D");
        queryParams.put("FID_ORG_ADJ_PRC", "0");

        UriComponentsBuilder uriBuilder = UriComponentsBuilder.fromHttpUrl(baseUrl);
        queryParams.forEach(uriBuilder::queryParam);
        String url = uriBuilder.toUriString();

        HttpEntity<?> requestMessage = new HttpEntity<>(httpHeaders);

        ResponseEntity<ChartResponseDto> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                requestMessage,
                ChartResponseDto.class);

        return response.getBody();
    }
}
