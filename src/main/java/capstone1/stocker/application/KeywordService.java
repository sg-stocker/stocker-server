package capstone1.stocker.application;

import capstone1.stocker.domain.Company;
import capstone1.stocker.domain.Keyword;
import capstone1.stocker.dto.KeywordResponseDto;
import capstone1.stocker.repository.CompanyRepository;
import capstone1.stocker.repository.KeywordRepository;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
@Slf4j
public class KeywordService {
    private final KeywordRepository keywordRepository;
    private final CompanyRepository companyRepository;

    public KeywordResponseDto readAllKeywordByCompany(String ticker){

        Company targetCompany = companyRepository.findByTicker(ticker)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));

        List<Keyword> result = keywordRepository.findAllByCompany(targetCompany);

        return KeywordResponseDto.builder()
                .keywords(result)
                .build();
    }
}
