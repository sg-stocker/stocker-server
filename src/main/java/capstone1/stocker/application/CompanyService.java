package capstone1.stocker.application;

import capstone1.stocker.domain.Company;
import capstone1.stocker.dto.CompanyResponse;
import capstone1.stocker.repository.CompanyRepository;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class CompanyService {
    private final CompanyRepository companyRepository;

    public CompanyResponse getAllCompanies(){
        HashMap resultMap = companyRepository.findAll().stream()
                .collect(Collectors.toMap(
                        Company::getName,
                        Company::getTicker,
                        (oldValue, newValue) -> oldValue,
                        HashMap::new
                ));
        return CompanyResponse.from(resultMap);

    }
}
