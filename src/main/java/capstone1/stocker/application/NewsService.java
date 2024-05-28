package capstone1.stocker.application;

import capstone1.stocker.domain.News;
import capstone1.stocker.dto.NewsDto;
import capstone1.stocker.repository.CompanyRepository;
import capstone1.stocker.repository.KeywordRepository;
import capstone1.stocker.repository.NewsRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
@Transactional
@RequiredArgsConstructor
public class NewsService {
    private final NewsRepository newsRepository;
    private final CompanyRepository companyRepository;
    private final KeywordRepository keywordRepository;

    @Value("${CLIENT_ID}")
    private String clientId;

    @Value("${CLIENT_SECRET}")
    private String clientSecret;

    public NewsDto getNews(Long keywordId) throws Exception {
        List<News> newsList = newsRepository.findNewsByKeywordId(keywordId);

        return NewsDto.builder()
                .news(newsList)
                .build();
    }

}
