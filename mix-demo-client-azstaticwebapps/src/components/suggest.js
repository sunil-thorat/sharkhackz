import React, { useState } from 'react'

import 'react-bootstrap-typeahead/css/Typeahead.css';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

import {ROOT_URL} from "./shared"

const suggestApiUrl = `${ROOT_URL}/api/suggest`

const Suggestions = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [options, setOptions] = useState([]);

  const handleSearch = (query) => {
    setIsLoading(true);

    fetch(`${suggestApiUrl}?q=${query}`)
      .then((resp) => resp.json())
      .then(({ suggestions }) => {
          if (!suggestions) {
              return
          }
          const options = suggestions.map(suggestion => {
              var boldChars = (suggestion.match(/%3A/g)).length
              if (boldChars > 0 && boldChars % 2 === 0) {
                  for (var index = 0; index < (boldChars / 2); index ++) {
                    suggestion = suggestion.replace("%3A", "<strong>")
                    suggestion = suggestion.replace("%3A", "</strong>")
                  }
              } else {
                suggestion = suggestion.replace(/%3A/g, "")
              }
              return suggestion
          }).map((suggestion) => ({
              id: suggestion,
              suggestion: suggestion
          }));
          setOptions(options);
          setIsLoading(false);
      });
  };

  // Bypass client-side filtering by returning `true`. Results are already
  // filtered by the search endpoint, so no need to do it again.
  const filterBy = () => true;

  return (
    <AsyncTypeahead
      filterBy={filterBy}
      id="suggestions"
      isLoading={isLoading}
      labelKey="suggestion"
      minLength={3}
      onSearch={handleSearch}
      options={options}
      placeholder="Type"
      selectHintOnEnter={true}
      delay={200}
      renderMenuItemChildren={(option, props) => (
          <span>{option.suggestion}</span>
      )}
    />
  );
};

export {Suggestions}